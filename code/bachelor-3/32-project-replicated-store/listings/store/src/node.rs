// node.rs: one replica as a process. A main loop owns the Raft state machine, the log
// file and the map; threads only move bytes: one per connection in, one per peer out.
use crate::protocol::{parse, Command, Reply};
use crate::raft::{Entry, Msg, Output, Raft, Role};
use crate::wal::Wal;
use std::collections::BTreeMap;
use std::io::{self, BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::path::PathBuf;
use std::sync::mpsc::{channel, Receiver, RecvTimeoutError, Sender};
use std::thread;
use std::time::{Duration, Instant};

pub fn address(base: u16, node: u32) -> String {
    format!("127.0.0.1:{}", base + node as u16)
}

pub struct Config {
    pub id: u32,
    pub nodes: u32,
    pub base: u16,
    pub dir: PathBuf,
    pub tick: Duration,
    pub timeouts: (u32, u32),
    pub batch: bool, // take every waiting event before forcing the log: one fsync for many
}

enum Event {
    Peer(u32, Msg),
    Client(Command, Sender<Reply>),
}

pub fn encode(msg: &Msg) -> String {
    match msg {
        Msg::RequestVote { term, last_index, last_term } => {
            format!("VOTE? {term} {last_index} {last_term}\n")
        }
        Msg::Vote { term, granted } => format!("VOTE {term} {}\n", *granted as u8),
        Msg::Append { term, prev_index, prev_term, entries, commit } => {
            let mut s = format!(
                "APPEND {term} {prev_index} {prev_term} {commit} {}\n",
                entries.len()
            );
            entries.iter().for_each(|e| s += &format!("{} {}\n", e.term, e.command));
            s
        }
        Msg::Appended { term, success, match_index } => {
            format!("APPENDED {term} {} {match_index}\n", *success as u8)
        }
    }
}

/// Reads one message from a peer's stream; None at the end of the stream or on garbage.
pub fn decode(reader: &mut impl BufRead) -> Option<Msg> {
    let mut line = String::new();
    if reader.read_line(&mut line).ok()? == 0 {
        return None;
    }
    let words: Vec<&str> = line.split_whitespace().collect();
    let n: Vec<u64> =
        words.iter().skip(1).map(|w| w.parse().ok()).collect::<Option<_>>()?;
    match (words.first()?, n.as_slice()) {
        (&"VOTE?", &[term, last_index, last_term]) => {
            Some(Msg::RequestVote { term, last_index, last_term })
        }
        (&"VOTE", &[term, g]) => Some(Msg::Vote { term, granted: g == 1 }),
        (&"APPENDED", &[term, s, match_index]) => {
            Some(Msg::Appended { term, success: s == 1, match_index })
        }
        (&"APPEND", &[term, prev_index, prev_term, commit, count]) => {
            let mut entries = Vec::new();
            for _ in 0..count {
                let mut l = String::new();
                reader.read_line(&mut l).ok()?;
                let (t, command) = l.trim_end().split_once(' ')?;
                entries.push(Entry {
                    term: t.parse().ok()?,
                    command: command.to_string(),
                });
            }
            Some(Msg::Append { term, prev_index, prev_term, entries, commit })
        }
        _ => None,
    }
}

/// A connection: a peer announces itself with "PEER n"; anything else is a client.
fn serve(stream: TcpStream, events: Sender<Event>) {
    let mut out = stream.try_clone().expect("clone");
    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    while matches!(reader.read_line(&mut line), Ok(n) if n > 0) {
        if let Some(peer) =
            line.strip_prefix("PEER ").and_then(|p| p.trim().parse().ok())
        {
            while let Some(msg) = decode(&mut reader) {
                if events.send(Event::Peer(peer, msg)).is_err() {
                    return;
                }
            }
            return;
        }
        let reply = match parse(line.trim_end()) {
            Err(reason) => Reply::Err(reason),
            Ok(command) => {
                let (tx, rx) = channel();
                if events.send(Event::Client(command, tx)).is_err() {
                    return;
                }
                rx.recv().unwrap_or(Reply::Err("node stopping".to_string()))
            }
        };
        if writeln!(out, "{reply}").is_err() {
            return;
        }
        line.clear();
    }
}

/// The messages to one peer: connect when needed; a message that cannot go is lost,
/// which Raft tolerates (the leader sends again at its next heartbeat).
fn sender(base: u16, me: u32, peer: u32, messages: Receiver<Msg>) {
    let mut stream: Option<TcpStream> = None;
    for msg in messages {
        if stream.is_none() {
            let addr = address(base, peer).parse().unwrap();
            stream =
                TcpStream::connect_timeout(&addr, Duration::from_millis(100)).ok();
            if let Some(s) = stream.as_mut() {
                let _ = s.set_nodelay(true);
                if writeln!(s, "PEER {me}").is_err() {
                    stream = None;
                }
            }
        }
        if let Some(s) = stream.as_mut() {
            if s.write_all(encode(&msg).as_bytes()).is_err() {
                stream = None;
            }
        }
    }
}

/// The state machine the log drives: a map. Returns the reply for the command's client.
fn apply(map: &mut BTreeMap<String, String>, command: &str) -> Reply {
    match parse(command) {
        Ok(Command::Set(k, v)) => {
            map.insert(k, v);
            Reply::Ok
        }
        Ok(Command::Del(k)) => map.remove(&k).map_or(Reply::NotFound, |_| Reply::Ok),
        _ => Reply::Ok, // NOOP
    }
}

pub fn run(cfg: Config) -> io::Result<()> {
    std::fs::create_dir_all(&cfg.dir)?;
    let (mut wal, records) = Wal::open(&cfg.dir.join("wal.log"))?;
    let peers: Vec<u32> = (1..=cfg.nodes).filter(|&p| p != cfg.id).collect();
    let mut raft = Raft::new(
        cfg.id,
        peers.clone(),
        &records,
        cfg.timeouts,
        7919 * cfg.id as u64,
    );
    let listener = TcpListener::bind(address(cfg.base, cfg.id))?;
    let (events, inbox) = channel();
    thread::spawn(move || {
        for stream in listener.incoming().flatten() {
            let events = events.clone();
            thread::spawn(move || serve(stream, events));
        }
    });
    let mut outbox = BTreeMap::new();
    for &p in &peers {
        let (tx, rx) = channel();
        outbox.insert(p, tx);
        let (base, me) = (cfg.base, cfg.id);
        thread::spawn(move || sender(base, me, p, rx));
    }
    println!(
        "node {}: up, {} entries in its log, term {}",
        cfg.id,
        raft.log.len(),
        raft.term
    );
    let mut map: BTreeMap<String, String> = BTreeMap::new();
    let mut pending: BTreeMap<u64, (u64, Sender<Reply>)> = BTreeMap::new();
    let mut role = raft.role;
    let mut next_tick = Instant::now() + cfg.tick;
    loop {
        let mut out = Output::default();
        let mut events = Vec::new();
        match inbox.recv_timeout(next_tick.saturating_duration_since(Instant::now()))
        {
            Ok(event) => events.push(event),
            Err(RecvTimeoutError::Timeout) => {}
            Err(RecvTimeoutError::Disconnected) => return Ok(()),
        }
        if Instant::now() >= next_tick {
            // time passes even when events never stop coming
            raft.tick(&mut out);
            next_tick += cfg.tick;
        }
        while cfg.batch && events.len() < 256 {
            match inbox.try_recv() {
                Ok(event) => events.push(event),
                Err(_) => break,
            }
        }
        for event in events {
            match event {
                Event::Peer(from, msg) => raft.receive(from, msg, &mut out),
                Event::Client(command, reply) => {
                    let answer = match (&command, raft.role) {
                        (Command::Status, _) => Some(Reply::Status(
                            format!("{:?}", raft.role).to_lowercase(),
                            raft.leader,
                        )),
                        (Command::Dump, _) => Some(Reply::Dump(
                            map.iter().map(|(k, v)| (k.clone(), v.clone())).collect(),
                        )),
                        (_, r) if r != Role::Leader => {
                            Some(Reply::Redirect(raft.leader))
                        }
                        (Command::Get(k), _) => Some(
                            map.get(k)
                                .map_or(Reply::NotFound, |v| Reply::Value(v.clone())),
                        ),
                        _ => {
                            let index =
                                raft.propose(command.to_string(), &mut out).unwrap();
                            pending.insert(index, (raft.term, reply.clone()));
                            None
                        }
                    };
                    if let Some(a) = answer {
                        let _ = reply.send(a);
                    }
                }
            }
        }
        wal.append(&out.persist)?; // on the disk before any message leaves
        for (to, msg) in out.send {
            let _ = outbox[&to].send(msg);
        }
        for (index, entry) in out.apply {
            let result = apply(&mut map, &entry.command);
            if let Some((term, client)) = pending.remove(&index) {
                let ok = term == entry.term;
                let _ = client.send(if ok {
                    result
                } else {
                    Reply::Err("unknown outcome".to_string())
                });
            }
        }
        if raft.role != role {
            role = raft.role;
            println!(
                "node {}: {} in term {}",
                cfg.id,
                format!("{role:?}").to_lowercase(),
                raft.term
            );
            if role != Role::Leader {
                for (_, (_, client)) in std::mem::take(&mut pending) {
                    let _ = client.send(Reply::Err("unknown outcome".to_string()));
                }
            }
        }
    }
}
