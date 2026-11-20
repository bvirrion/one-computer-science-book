// mset.rs (exercise 10): MSET and MGET across shards, the shard locks taken in
// increasing order of shard number.
use crate::store::{shard_of, Sharded};

/// The shard numbers of the keys, sorted, each once.
fn ordered(store: &Sharded, keys: &[&str]) -> Vec<usize> {
    let mut ids: Vec<usize> = keys.iter().map(|k| shard_of(k, store.shards().len())).collect();
    ids.sort();
    ids.dedup();
    ids
}

/// Set every pair, all or nothing as seen by any MGET.
pub fn mset(store: &Sharded, pairs: &[(&str, &str)]) {
    let keys: Vec<&str> = pairs.iter().map(|(k, _)| *k).collect();
    let ids = ordered(store, &keys);
    let mut held: Vec<_> = ids.iter().map(|&i| store.shards()[i].write().unwrap()).collect();
    for (k, v) in pairs {
        let at = ids.binary_search(&shard_of(k, store.shards().len())).unwrap();
        held[at].insert(k.to_string(), v.to_string());
    }
}

/// Read every key at one instant: all the shard locks are held together.
pub fn mget(store: &Sharded, keys: &[&str]) -> Vec<Option<String>> {
    let ids = ordered(store, keys);
    let held: Vec<_> = ids.iter().map(|&i| store.shards()[i].read().unwrap()).collect();
    keys.iter()
        .map(|k| {
            let at = ids.binary_search(&shard_of(k, store.shards().len())).unwrap();
            held[at].get(*k).cloned()
        })
        .collect()
}
