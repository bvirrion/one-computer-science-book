//! Tests of chapter 31: the protocol, the stores under concurrent clients, replay
//! and compaction, the torn tail, and MSET with ordered locking under load.
#[path = "../../../listings/client.rs"]
pub mod client;
#[path = "../../../listings/log.rs"]
pub mod log;
#[path = "../../../exercises/mset.rs"]
pub mod mset;
#[path = "../../../listings/protocol.rs"]
pub mod protocol;
#[path = "../../../listings/server.rs"]
pub mod server;
#[path = "../../../listings/store.rs"]
pub mod store;

#[cfg(test)]
mod tests {
    use super::log::{crc32, record, replay, Flush, Log};
    use super::protocol::{parse, Command, Reply, MAX_LINE};
    use super::store::{Map, OneLock, Sharded, Store};
    use std::sync::Arc;
    use std::thread;

    /// A seeded generator, so that every run tests the same cases.
    struct Lcg(u64);
    impl Lcg {
        fn below(&mut self, n: u64) -> u64 {
            self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (self.0 >> 33) % n
        }
        fn command(&mut self, keys: u64) -> Command {
            let key = format!("k{}", self.below(keys));
            match self.below(4) {
                0 => Command::Del(key),
                1 => Command::Get(key),
                _ => Command::Set(key, format!("v{}", self.below(100))),
            }
        }
    }

    fn model(cmds: &[Command]) -> Map {
        let mut m = Map::new();
        for c in cmds {
            match c {
                Command::Set(k, v) => {
                    m.insert(k.clone(), v.clone());
                }
                Command::Del(k) => {
                    m.remove(k);
                }
                _ => {}
            }
        }
        m
    }

    #[test]
    fn parses_every_command_and_every_malformed_line() {
        assert_eq!(parse("SET a 1"), Ok(Command::Set("a".into(), "1".into())));
        assert_eq!(parse("GET a"), Ok(Command::Get("a".into())));
        assert_eq!(parse("DEL a"), Ok(Command::Del("a".into())));
        assert_eq!(parse("COUNT"), Ok(Command::Count));
        assert_eq!(parse("QUIT"), Ok(Command::Quit));
        let bad = [
            ("", "empty line"),
            ("set a 1", "unknown command set"),
            ("PUT a 1", "unknown command PUT"),
            ("SET a", "SET takes a key and a value"),
            ("SET a 1 2", "SET takes a key and a value"),
            ("SET", "SET takes a key and a value"),
            ("GET", "GET takes one key"),
            ("GET a b", "GET takes one key"),
            ("DEL", "DEL takes one key"),
            ("COUNT x", "COUNT takes no argument"),
            ("QUIT now", "QUIT takes no argument"),
        ];
        for (line, reason) in bad {
            assert_eq!(parse(line), Err(reason.to_string()), "{line:?}");
        }
        let long = format!("SET a {}", "x".repeat(MAX_LINE));
        assert_eq!(parse(&long), Err(format!("line longer than {MAX_LINE} bytes")));
    }

    #[test]
    fn printing_then_parsing_gives_the_command_back() {
        let mut rng = Lcg(1);
        for _ in 0..1000 {
            let c = rng.command(50);
            assert_eq!(parse(&c.to_string()), Ok(c));
        }
        assert_eq!(Reply::Value("x".into()).to_string(), "VALUE x");
        assert_eq!(Reply::Err("why".into()).to_string(), "ERR why");
    }

    #[test]
    fn both_stores_agree_with_a_plain_map() {
        let mut rng = Lcg(2);
        let cmds: Vec<Command> = (0..3000).map(|_| rng.command(40)).collect();
        let (one, many) = (OneLock::new(Map::new()), Sharded::new(16, Map::new()));
        let mut m = Map::new();
        for c in &cmds {
            let expected = match c {
                Command::Get(k) => m.get(k).map_or(Reply::NotFound, |v| Reply::Value(v.clone())),
                Command::Del(k) => m.remove(k).map_or(Reply::NotFound, |_| Reply::Ok),
                Command::Set(k, v) => {
                    m.insert(k.clone(), v.clone());
                    Reply::Ok
                }
                _ => unreachable!(),
            };
            assert_eq!(one.apply(c, None), expected);
            assert_eq!(many.apply(c, None), expected);
        }
        assert_eq!(many.apply(&Command::Count, None), Reply::Count(m.len()));
    }

    #[test]
    fn concurrent_clients_lose_nothing() {
        for store in [
            Arc::new(OneLock::new(Map::new())) as Arc<dyn Store>,
            Arc::new(Sharded::new(16, Map::new())),
        ] {
            let threads: Vec<_> = (0..8)
                .map(|t| {
                    let s = Arc::clone(&store);
                    thread::spawn(move || {
                        for i in 0..1000 {
                            s.apply(&Command::Set(format!("t{t}k{i}"), format!("{i}")), None);
                        }
                    })
                })
                .collect();
            threads.into_iter().for_each(|h| h.join().unwrap());
            assert_eq!(store.apply(&Command::Count, None), Reply::Count(8000));
            assert_eq!(store.apply(&Command::Get("t7k999".into()), None), Reply::Value("999".into()));
        }
    }

    #[test]
    fn crc32_check_value() {
        assert_eq!(crc32(b"123456789"), 0xCBF4_3926);
        assert_eq!(crc32(b""), 0);
    }

    /// The replay proposition: cut the log anywhere; replay gives the map after
    /// the last record that is wholly before the cut.
    #[test]
    fn replay_of_every_prefix_is_the_map_after_the_last_complete_record() {
        let mut rng = Lcg(3);
        let cmds: Vec<Command> = (0..200)
            .map(|_| rng.command(20))
            .filter(|c| !matches!(c, Command::Get(_)))
            .collect();
        let mut bytes = Vec::new();
        let mut ends = vec![0];
        for c in &cmds {
            bytes.extend(record(c));
            ends.push(bytes.len());
        }
        for cut in 0..=bytes.len() {
            let complete = ends.iter().rposition(|&e| e <= cut).unwrap();
            let (map, r) = replay(&bytes[..cut]);
            assert_eq!(map, model(&cmds[..complete]), "cut at {cut}");
            assert_eq!(r.records, complete);
            assert_eq!(r.kept_bytes as usize, ends[complete]);
        }
    }

    #[test]
    fn a_corrupted_byte_stops_the_replay_at_its_record() {
        let cmds: Vec<Command> =
            (0..10).map(|i| Command::Set(format!("k{i}"), format!("v{i}"))).collect();
        let bytes: Vec<u8> = cmds.iter().flat_map(record).collect();
        let size = record(&cmds[0]).len();
        for at in 0..bytes.len() {
            let mut damaged = bytes.clone();
            damaged[at] ^= 0x10;
            let (map, r) = replay(&damaged);
            assert_eq!(r.records, at / size, "byte {at}");
            assert_eq!(map, model(&cmds[..at / size]));
        }
    }

    fn scratch(name: &str) -> std::path::PathBuf {
        let dir = std::env::temp_dir().join(format!("kv-unit-{}-{name}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        dir.join("kv.log")
    }

    #[test]
    fn open_cuts_the_torn_tail_and_appends_after_the_last_good_record() {
        let path = scratch("torn");
        let (mut log, _, _) = Log::open(&path, Flush::Never).unwrap();
        log.append(&Command::Set("a".into(), "1".into())).unwrap();
        drop(log);
        let torn = record(&Command::Set("b".into(), "2".into()));
        let mut bytes = std::fs::read(&path).unwrap();
        bytes.extend(&torn[..5]);
        std::fs::write(&path, &bytes).unwrap();
        let (mut log, map, r) = Log::open(&path, Flush::Never).unwrap();
        assert_eq!((map.len(), r.records, r.dropped_bytes), (1, 1, 5));
        log.append(&Command::Set("c".into(), "3".into())).unwrap();
        let (map, r) = replay(&std::fs::read(&path).unwrap());
        assert_eq!((map.len(), r.records, r.dropped_bytes), (2, 2, 0));
        std::fs::remove_file(&path).unwrap();
        std::fs::remove_dir(path.parent().unwrap()).unwrap();
    }

    /// The compaction proposition, through the store's own compaction.
    #[test]
    fn the_compacted_log_replays_to_the_same_map() {
        let path = scratch("compact");
        let (log, _, _) = Log::open(&path, Flush::Never).unwrap();
        let log = std::sync::Mutex::new(log);
        let store = Sharded::new(16, Map::new());
        let mut rng = Lcg(4);
        let cmds: Vec<Command> = (0..2000).map(|_| rng.command(30)).collect();
        for c in &cmds {
            store.apply(c, Some(&log));
        }
        let before = std::fs::read(&path).unwrap();
        let size = store.compact(&log).unwrap();
        let after = std::fs::read(&path).unwrap();
        assert_eq!(replay(&before).0, replay(&after).0);
        assert_eq!(replay(&after).0, model(&cmds));
        assert_eq!(size as usize, after.len());
        assert!(after.len() < before.len());
        store.apply(&Command::Set("new".into(), "1".into()), Some(&log));
        assert_eq!(replay(&std::fs::read(&path).unwrap()).0.len(), model(&cmds).len() + 1);
        std::fs::remove_file(&path).unwrap();
        std::fs::remove_dir(path.parent().unwrap()).unwrap();
    }

    /// Exercise 10: MSET under load; every MGET sees both keys from the same MSET.
    #[test]
    fn mset_is_atomic_under_load() {
        use super::mset::{mget, mset};
        let store = Arc::new(Sharded::new(16, Map::new()));
        let keys = ["left", "right", "middle"];
        mset(&store, &[("left", "0"), ("right", "0"), ("middle", "0")]);
        let writers: Vec<_> = (0..4)
            .map(|t| {
                let s = Arc::clone(&store);
                thread::spawn(move || {
                    for i in 0..2000 {
                        let v = format!("{t}-{i}");
                        // each writer names the keys in its own order
                        let mut pairs = vec![("left", v.as_str()), ("right", &v), ("middle", &v)];
                        pairs.rotate_left(t % 3);
                        mset(&s, &pairs);
                    }
                })
            })
            .collect();
        let readers: Vec<_> = (0..4)
            .map(|_| {
                let s = Arc::clone(&store);
                thread::spawn(move || {
                    for _ in 0..5000 {
                        let got = mget(&s, &keys);
                        assert!(got.iter().all(|v| *v == got[0]), "{got:?}");
                    }
                })
            })
            .collect();
        writers.into_iter().chain(readers).for_each(|h| h.join().unwrap());
    }
}
