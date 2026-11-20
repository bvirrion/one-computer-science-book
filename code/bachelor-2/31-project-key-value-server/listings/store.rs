// store.rs: the map, behind one Mutex or sharded behind N RwLocks.
use crate::log::Log;
use crate::protocol::{Command, Reply};
use std::collections::hash_map::DefaultHasher;
use std::collections::HashMap;
use std::hash::{Hash, Hasher};
use std::io;
use std::sync::{Mutex, RwLock};

pub type Map = HashMap<String, String>;

/// What every store does; Send + Sync so that threads can share it.
pub trait Store: Send + Sync {
    /// Run one command; a SET or DEL is appended to the log, if any, under the
    /// same lock as the change, so that the log order is the order of changes.
    fn apply(&self, cmd: &Command, log: Option<&Mutex<Log>>) -> Reply;
    /// Rewrite the log as one SET per key, no write allowed meanwhile.
    fn compact(&self, log: &Mutex<Log>) -> io::Result<u64>;
}

/// SET or DEL on a map the caller has locked: log first, then change.
pub fn write(map: &mut Map, cmd: &Command, log: Option<&Mutex<Log>>) -> Reply {
    if let Command::Del(k) = cmd {
        if !map.contains_key(k) {
            return Reply::NotFound; // nothing changes: nothing to log
        }
    }
    if let Some(log) = log {
        if log.lock().unwrap().append(cmd).is_err() {
            return Reply::Err("log write failed".to_string());
        }
    }
    match cmd {
        Command::Set(k, v) => {
            map.insert(k.clone(), v.clone());
            Reply::Ok
        }
        Command::Del(k) => {
            map.remove(k);
            Reply::Ok
        }
        _ => unreachable!("write is called for SET and DEL only"),
    }
}

pub fn read(map: &Map, key: &str) -> Reply {
    match map.get(key) {
        Some(v) => Reply::Value(v.clone()),
        None => Reply::NotFound,
    }
}

pub struct OneLock {
    map: Mutex<Map>,
}

impl OneLock {
    pub fn new(map: Map) -> OneLock {
        OneLock { map: Mutex::new(map) }
    }
}

impl Store for OneLock {
    fn apply(&self, cmd: &Command, log: Option<&Mutex<Log>>) -> Reply {
        let mut map = self.map.lock().unwrap();
        match cmd {
            Command::Get(k) => read(&map, k),
            Command::Count => Reply::Count(map.len()),
            Command::Quit => Reply::Ok,
            _ => write(&mut map, cmd, log),
        }
    }

    fn compact(&self, log: &Mutex<Log>) -> io::Result<u64> {
        let map = self.map.lock().unwrap();
        log.lock().unwrap().rewrite(&[&*map])
    }
}

pub struct Sharded {
    shards: Vec<RwLock<Map>>,
}

/// The shard of a key: a hash of the key, modulo the number of shards.
pub fn shard_of(key: &str, n: usize) -> usize {
    let mut h = DefaultHasher::new();
    key.hash(&mut h);
    (h.finish() % n as u64) as usize
}

impl Sharded {
    pub fn new(n: usize, map: Map) -> Sharded {
        let mut parts: Vec<Map> = (0..n).map(|_| Map::new()).collect();
        for (k, v) in map {
            parts[shard_of(&k, n)].insert(k, v);
        }
        Sharded { shards: parts.into_iter().map(RwLock::new).collect() }
    }

    pub fn shard(&self, key: &str) -> &RwLock<Map> {
        &self.shards[shard_of(key, self.shards.len())]
    }

    pub fn shards(&self) -> &[RwLock<Map>] {
        &self.shards
    }
}

impl Store for Sharded {
    fn apply(&self, cmd: &Command, log: Option<&Mutex<Log>>) -> Reply {
        match cmd {
            Command::Get(k) => read(&self.shard(k).read().unwrap(), k),
            Command::Set(k, _) | Command::Del(k) => {
                write(&mut self.shard(k).write().unwrap(), cmd, log)
            }
            // The shards are read in increasing order, one at a time.
            Command::Count => {
                Reply::Count(self.shards.iter().map(|s| s.read().unwrap().len()).sum())
            }
            Command::Quit => Reply::Ok,
        }
    }

    fn compact(&self, log: &Mutex<Log>) -> io::Result<u64> {
        // Every shard, in increasing order, then the log: the global lock order.
        let held: Vec<_> = self.shards.iter().map(|s| s.read().unwrap()).collect();
        let maps: Vec<&Map> = held.iter().map(|g| &**g).collect();
        log.lock().unwrap().rewrite(&maps)
    }
}
