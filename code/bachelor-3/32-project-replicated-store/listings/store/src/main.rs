// main.rs: the command line. `store node 2` runs replica 2; the other subcommands are
// clients and tools: send, wait-leader, dump, load, check, bench, sim.
use std::io::Write;
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};
use store::client::{ask, ask_leader};
use store::lincheck::{check, parse_line};
use store::node::{run, Config};
use store::protocol::{parse, Command, Reply};
use store::sim::{self, Rng, Settings};

fn flag<T: std::str::FromStr>(args: &[String], name: &str, default: T) -> T {
    args.iter()
        .position(|a| a == name)
        .and_then(|i| args.get(i + 1))
        .and_then(|v| v.parse().ok())
        .unwrap_or(default)
}

fn status(base: u16, node: u32) -> Option<(String, u32)> {
    match ask(base, node, &Command::Status) {
        Ok(Reply::Status(role, leader)) => Some((role, leader)),
        _ => None,
    }
}

/// The leader, once a node says it leads and every other node that answers agrees.
fn wait_leader(base: u16, nodes: u32) -> Option<u32> {
    let start = Instant::now();
    while start.elapsed() < Duration::from_secs(15) {
        let seen: Vec<(u32, (String, u32))> =
            (1..=nodes).filter_map(|n| status(base, n).map(|s| (n, s))).collect();
        if let Some(&(leader, _)) =
            seen.iter().find(|(_, (role, _))| role == "leader")
        {
            if seen.iter().all(|(n, (_, l))| *n == leader || *l == leader) {
                return Some(leader);
            }
        }
        thread::sleep(Duration::from_millis(50));
    }
    None
}

fn dump(base: u16, node: u32) -> Option<Vec<(String, String)>> {
    match ask(base, node, &Command::Dump) {
        Ok(Reply::Dump(pairs)) => Some(pairs),
        _ => None,
    }
}

/// `clients` threads, `ops` operations each, on `keys` keys; every operation recorded.
fn load(base: u16, nodes: u32, clients: u32, ops: u32, keys: u64) -> Vec<String> {
    let clock = Instant::now();
    let lines = Arc::new(Mutex::new(Vec::new()));
    let threads: Vec<_> = (1..=clients)
        .map(|c| {
            let lines = Arc::clone(&lines);
            thread::spawn(move || {
                let (mut rng, mut node) = (Rng::new(c as u64), c % nodes + 1);
                for n in 0..ops {
                    let key = format!("k{}", rng.below(keys));
                    let command = match rng.below(10) {
                        0..=4 => Command::Set(key.clone(), format!("c{c}n{n}")),
                        5..=7 => Command::Get(key.clone()),
                        _ => Command::Del(key.clone()),
                    };
                    let start = clock.elapsed().as_micros();
                    let trail = ask_leader(base, node, &command, 4);
                    let end = clock.elapsed().as_micros();
                    let (last, reply) = trail.last().unwrap();
                    node = *last;
                    let result = match (&command, reply) {
                        (Command::Set(_, v), Ok(Reply::Ok)) => {
                            Some(format!("SET {v}"))
                        }
                        (Command::Get(_), Ok(Reply::Value(v))) => {
                            Some(format!("GET {v}"))
                        }
                        (Command::Get(_), Ok(Reply::NotFound)) => {
                            Some("GET -".to_string())
                        }
                        (Command::Del(_), Ok(Reply::Ok)) => {
                            Some("DEL found".to_string())
                        }
                        (Command::Del(_), Ok(Reply::NotFound)) => {
                            Some("DEL notfound".to_string())
                        }
                        _ => None, // no answer: the outcome is unknown
                    };
                    let line = match (result, &command) {
                        (Some(r), _) => format!("{c} {start} {end} {key} {r}"),
                        (None, Command::Set(_, v)) => {
                            format!("{c} {start} ? {key} SET {v}")
                        }
                        (None, Command::Del(_)) => {
                            format!("{c} {start} ? {key} DEL ?")
                        }
                        (None, _) => format!("{c} {start} ? {key} GET -"),
                    };
                    if line.contains(" ? ") {
                        node = node % nodes + 1; // try another node next time
                        thread::sleep(Duration::from_millis(50));
                    }
                    lines.lock().unwrap().push(line);
                }
            })
        })
        .collect();
    threads.into_iter().for_each(|t| t.join().unwrap());
    Arc::try_unwrap(lines).unwrap().into_inner().unwrap()
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let base = flag(&args, "--base", 24320u16);
    let nodes = flag(&args, "--nodes", 3u32);
    let arg = |i: usize| args.get(i).cloned().unwrap_or_default();
    match arg(0).as_str() {
        "node" => {
            let id: u32 = arg(1).parse().expect("store node <id>");
            // --stagger: node n waits about 100 + 200(n - 1) ms before standing for
            // election, so that a session's leader is predictable; otherwise random.
            let timeouts = if args.iter().any(|a| a == "--stagger") {
                (10 + 20 * (id - 1), 12 + 20 * (id - 1))
            } else {
                (15, 30)
            };
            let dir = PathBuf::from(flag(&args, "--dir", format!("node{id}")));
            std::fs::create_dir_all(&dir)
                .and_then(|_| std::fs::write(dir.join("pid"), format!("{}\n", std::process::id())))
                .expect("data directory");
            let batch = args.iter().any(|a| a == "--batch");
            let cfg =
                Config { id, nodes, base, dir, tick: Duration::from_millis(10), timeouts, batch };
            if let Err(e) = run(cfg) {
                eprintln!("node {id}: {e}");
                std::process::exit(1);
            }
        }
        "send" => {
            let line = args[2..]
                .iter()
                .take_while(|a| !a.starts_with("--"))
                .cloned()
                .collect::<Vec<_>>()
                .join(" ");
            let command = parse(&line).unwrap_or_else(|e| panic!("{e}"));
            for (node, reply) in ask_leader(base, arg(1).parse().unwrap(), &command, 4) {
                match reply {
                    Ok(r) => println!("node {node}: {r}"),
                    Err(_) => println!("node {node}: no answer"),
                }
            }
        }
        "wait-leader" => match wait_leader(base, nodes) {
            Some(n) => println!("leader: node {n}"),
            None => println!("no leader after 15 s"),
        },
        "dump" => match dump(base, arg(1).parse().unwrap()) {
            Some(pairs) => println!(
                "node {}: {}",
                arg(1),
                pairs.iter().map(|(k, v)| format!("{k}={v}")).collect::<Vec<_>>().join(" ")
            ),
            None => println!("node {}: no answer", arg(1)),
        },
        "caught-up" => {
            // waits until a node's map equals the leader's
            let (node, start) = (arg(1).parse().unwrap(), Instant::now());
            while start.elapsed() < Duration::from_secs(15) {
                let leader = wait_leader(base, nodes).unwrap();
                if let (Some(a), Some(b)) = (dump(base, node), dump(base, leader)) {
                    if a == b {
                        println!(
                            "node {node} holds the same {} keys as the leader, node {leader}",
                            a.len()
                        );
                        return;
                    }
                }
                thread::sleep(Duration::from_millis(50));
            }
            println!("node {node} is still behind after 15 s");
        }
        "load" => {
            let (clients, ops, keys) =
                (flag(&args, "--clients", 4), flag(&args, "--ops", 100), flag(&args, "--keys", 3));
            let lines = load(base, nodes, clients, ops, keys);
            let mut file = std::fs::File::create(arg(1)).unwrap();
            lines.iter().for_each(|l| writeln!(file, "{l}").unwrap());
            println!(
                "{} operations by {clients} clients on {keys} keys recorded in {}",
                lines.len(),
                arg(1)
            );
        }
        "check" => {
            let text = std::fs::read_to_string(arg(1)).unwrap();
            let ops: Vec<_> = text.lines().map(|l| parse_line(l).expect("history line")).collect();
            let result = check(&ops);
            let bad: Vec<_> =
                result.iter().filter(|(_, &ok)| !ok).map(|(k, _)| k.as_str()).collect();
            println!(
                "{} operations on {} keys: linearisable: {}",
                ops.len(),
                result.len(),
                if bad.is_empty() {
                    "yes".to_string()
                } else {
                    format!("no, keys {}", bad.join(" "))
                }
            );
        }
        "bench" => {
            let (clients, secs) = (flag(&args, "--clients", 4u32), flag(&args, "--seconds", 3u64));
            let leader = wait_leader(base, nodes).unwrap();
            let done = Arc::new(Mutex::new(0u64));
            let start = Instant::now();
            let threads: Vec<_> = (0..clients)
                .map(|c| {
                    let done = Arc::clone(&done);
                    thread::spawn(move || {
                        let mut n = 0;
                        while start.elapsed() < Duration::from_secs(secs) {
                            if let Ok(Reply::Ok) =
                                ask(base, leader, &Command::Set(format!("b{c}"), format!("{n}")))
                            {
                                n += 1;
                            }
                        }
                        *done.lock().unwrap() += n;
                    })
                })
                .collect();
            threads.into_iter().for_each(|t| t.join().unwrap());
            let n = *done.lock().unwrap();
            println!(
                "{nodes} replica(s), {clients} clients, {secs} s: {n} writes, {} writes per second",
                n / secs
            );
        }
        "sim" => {
            let (runs, ticks) = (flag(&args, "--runs", 1000u64), flag(&args, "--ticks", 400u32));
            let mut s = Settings::new(ticks, flag(&args, "--loss", 50), flag(&args, "--crash", 2));
            s.nodes = nodes;
            let (mut elections, mut committed, mut crashes, mut violations) = (0, 0, 0, 0);
            for seed in 1..=runs {
                let r = sim::run(seed, &s);
                (elections, committed, crashes) =
                    (elections + r.elections, committed + r.committed, crashes + r.crashes);
                violations += r.violations.len();
                r.violations.iter().take(3).for_each(|v| println!("seed {seed}: {v}"));
            }
            println!(
                "{runs} runs of {ticks} ticks, {nodes} nodes, {} % of messages lost:",
                s.loss_permille as f64 / 10.0
            );
            println!(
                "  {crashes} crashes, {elections} leaders elected, {committed} entries committed"
            );
            println!("  safety violations: {violations}");
        }
        "trace" => {
            let mut s = Settings::new(
                flag(&args, "--ticks", 400),
                flag(&args, "--loss", 50),
                flag(&args, "--crash", 2),
            );
            s.nodes = nodes;
            let r = sim::run(arg(1).parse().unwrap(), &s);
            r.events.iter().for_each(|e| println!("{e}"));
            println!(
                "{} entries committed, safety violations: {}",
                r.committed,
                r.violations.len()
            );
        }
        _ => eprintln!(
            "usage: store node|send|wait-leader|dump|caught-up|load|check|bench|sim|trace ..."
        ),
    }
}
