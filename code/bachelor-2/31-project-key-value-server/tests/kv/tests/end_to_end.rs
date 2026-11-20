//! The server as a program on 127.0.0.1:44311: a session, a restart, a compaction-free replay,
//! and a crash: the server killed while a client writes.
use kv::client::Client;
use kv::log::replay;
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::thread;
use std::time::Duration;

/// The server process, killed when the test ends, even when it fails.
struct Server(Child);

impl Server {
    fn kill(&mut self) {
        let _ = self.0.kill(); // SIGKILL: no clean-up runs in the server
        let _ = self.0.wait();
    }
}

impl Drop for Server {
    fn drop(&mut self) {
        self.kill();
    }
}

fn start(port: u16, log: &PathBuf) -> Server {
    let child = Command::new(env!("CARGO_BIN_EXE_kvserver"))
        .arg(port.to_string())
        .arg(log)
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .unwrap();
    Server(child)
}

fn scratch(name: &str) -> PathBuf {
    let dir = std::env::temp_dir().join(format!("kv-e2e-{}-{name}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    dir.join("kv.log")
}

fn clean(log: &PathBuf) {
    let _ = std::fs::remove_file(log);
    std::fs::remove_dir(log.parent().unwrap()).unwrap();
}

#[test]
fn a_session_survives_a_restart() {
    let log = scratch("session");
    let mut server = start(44311, &log);
    let mut c = Client::connect("127.0.0.1:44311").unwrap();
    for (line, reply) in [
        ("SET a 1", "OK"), ("SET b 2", "OK"), ("GET a", "VALUE 1"), ("DEL b", "OK"),
        ("DEL b", "NOTFOUND"), ("COUNT", "COUNT 1"), ("FROB", "ERR unknown command FROB"),
        ("QUIT", "OK"),
    ] {
        assert_eq!(c.request(line).unwrap(), reply, "{line}");
    }
    // A second client, while the first is gone; then a request in two writes.
    let mut d = Client::connect("127.0.0.1:44311").unwrap();
    d.write_raw(b"SET c").unwrap();
    thread::sleep(Duration::from_millis(50));
    assert_eq!(d.request(" 3").unwrap(), "OK");
    server.kill();

    let mut server = start(44311, &log);
    let mut c = Client::connect("127.0.0.1:44311").unwrap();
    assert_eq!(c.request("GET a").unwrap(), "VALUE 1");
    assert_eq!(c.request("GET b").unwrap(), "NOTFOUND");
    assert_eq!(c.request("GET c").unwrap(), "VALUE 3");
    server.kill();
    clean(&log);
}

#[test]
fn every_acknowledged_set_survives_a_kill() {
    let log = scratch("crash");
    let mut server = start(44313, &log);
    let writer = thread::spawn(|| {
        let mut c = Client::connect("127.0.0.1:44313").unwrap();
        let mut acknowledged = 0;
        for i in 0.. {
            match c.request(&format!("SET k{i} v{i}")) {
                Ok(reply) if reply == "OK" => acknowledged = i + 1,
                _ => break, // the server is gone
            }
        }
        acknowledged
    });
    thread::sleep(Duration::from_millis(300));
    server.kill(); // in the middle of the stream
    let acknowledged = writer.join().unwrap();
    let (map, recovery) = replay(&std::fs::read(&log).unwrap());
    assert!(acknowledged > 0);
    // Every acknowledged SET is there; at most one more, sent but not acknowledged.
    assert!(recovery.records == acknowledged || recovery.records == acknowledged + 1);
    for i in 0..recovery.records {
        assert_eq!(map.get(&format!("k{i}")), Some(&format!("v{i}")));
    }
    clean(&log);
}
