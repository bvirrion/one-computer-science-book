// Three real processes on 127.0.0.1: a leader elected, writes, the leader killed, a new
// leader with every acknowledged write, the old leader back and caught up, and a
// recorded history under a kill found linearisable.
use std::path::Path;
use std::process::{Child, Command as Proc, Stdio};
use std::time::Duration;
use store::client::{ask, ask_leader};
use store::lincheck::{check, parse_line};
use store::protocol::{Command, Reply};

const BASE: u16 = 24370;

fn start(dir: &Path, id: u32) -> Child {
    Proc::new(env!("CARGO_BIN_EXE_store"))
        .args(["node", &id.to_string(), "--stagger", "--base", &BASE.to_string()])
        .arg("--dir")
        .arg(dir.join(format!("node{id}")))
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .unwrap()
}

fn leader() -> u32 {
    for _ in 0..300 {
        for n in 1..=3 {
            if let Ok(Reply::Status(role, _)) = ask(BASE, n, &Command::Status) {
                if role == "leader" {
                    return n;
                }
            }
        }
        std::thread::sleep(Duration::from_millis(50));
    }
    panic!("no leader");
}

fn send(node: u32, c: Command) -> Reply {
    ask_leader(BASE, node, &c, 4).pop().unwrap().1.unwrap()
}

#[test]
fn kill_the_leader() {
    let dir =
        std::env::temp_dir().join(format!("store-cluster-{}", std::process::id()));
    let mut nodes: Vec<Child> = (1..=3).map(|id| start(&dir, id)).collect();
    let first = leader();
    for i in 0..20 {
        assert_eq!(
            send(1 + i % 3, Command::Set(format!("k{i}"), format!("{i}"))),
            Reply::Ok
        );
    }
    nodes[first as usize - 1].kill().unwrap();
    nodes[first as usize - 1].wait().unwrap();
    std::thread::sleep(Duration::from_millis(300));
    let second = leader();
    assert_ne!(second, first);
    for i in 0..20 {
        assert_eq!(
            send(second, Command::Get(format!("k{i}"))),
            Reply::Value(format!("{i}"))
        );
    }
    assert_eq!(send(second, Command::Set("after".into(), "kill".into())), Reply::Ok);
    nodes[first as usize - 1] = start(&dir, first);
    let mut caught_up = false;
    for _ in 0..200 {
        if let Ok(Reply::Dump(pairs)) = ask(BASE, first, &Command::Dump) {
            if pairs.len() == 21 && pairs.contains(&("after".into(), "kill".into())) {
                caught_up = true;
                break;
            }
        }
        std::thread::sleep(Duration::from_millis(50));
    }
    assert!(caught_up);
    for mut n in nodes {
        n.kill().unwrap();
        n.wait().unwrap();
    }
    std::fs::remove_dir_all(&dir).unwrap();
}

#[test]
fn history_under_a_kill_is_linearisable() {
    let dir =
        std::env::temp_dir().join(format!("store-history-{}", std::process::id()));
    let base = BASE + 10;
    let start = |id: u32| {
        Proc::new(env!("CARGO_BIN_EXE_store"))
            .args(["node", &id.to_string(), "--stagger", "--base", &base.to_string()])
            .arg("--dir")
            .arg(dir.join(format!("node{id}")))
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .unwrap()
    };
    let mut nodes: Vec<Child> = (1..=3).map(start).collect();
    let wait = Proc::new(env!("CARGO_BIN_EXE_store"))
        .args(["wait-leader", "--base", &base.to_string()])
        .output()
        .unwrap();
    assert_eq!(String::from_utf8_lossy(&wait.stdout), "leader: node 1\n");
    let history = dir.join("h.txt");
    let load = Proc::new(env!("CARGO_BIN_EXE_store"))
        .args([
            "load",
            history.to_str().unwrap(),
            "--clients",
            "4",
            "--ops",
            "150",
            "--base",
            &base.to_string(),
        ])
        .stdout(Stdio::null())
        .spawn()
        .unwrap();
    std::thread::sleep(Duration::from_millis(400));
    nodes[0].kill().unwrap();
    nodes[0].wait().unwrap();
    assert!(load.wait_with_output().unwrap().status.success());
    let text = std::fs::read_to_string(&history).unwrap();
    let ops: Vec<_> = text.lines().map(|l| parse_line(l).unwrap()).collect();
    assert_eq!(ops.len(), 600);
    assert!(check(&ops).values().all(|&v| v));
    for mut n in nodes.into_iter().skip(1) {
        n.kill().unwrap();
        n.wait().unwrap();
    }
    std::fs::remove_dir_all(&dir).unwrap();
}
