// lincheck.rs: is a recorded history of a key-value store linearisable? Each key is a
// register, checked on its own (linearisability is local). For one key, the search of
// the concurrency chapter: pick an operation that may come first, apply it to the
// sequential register, recurse; with the states already refuted remembered.
use std::collections::{BTreeMap, HashSet};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Kind {
    Set(String),
    Get(Option<String>), // the value read, None for NOTFOUND
    Del(Option<bool>),   // found or not; None when the outcome is unknown
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Op {
    pub client: u32,
    pub key: String,
    pub kind: Kind,
    pub start: u64,
    pub end: Option<u64>, // None: no reply came, the operation may or may not have happened
}

/// One line of a history file: client start end key SET v | GET v | GET - | DEL found|notfound|?
pub fn parse_line(line: &str) -> Option<Op> {
    let w: Vec<&str> = line.split_whitespace().collect();
    let end = if w.get(2)? == &"?" { None } else { Some(w[2].parse().ok()?) };
    let kind = match (*w.get(4)?, w.get(5).copied()) {
        ("SET", Some(v)) => Kind::Set(v.to_string()),
        ("GET", Some("-")) => Kind::Get(None),
        ("GET", Some(v)) => Kind::Get(Some(v.to_string())),
        ("DEL", Some("found")) => Kind::Del(Some(true)),
        ("DEL", Some("notfound")) => Kind::Del(Some(false)),
        ("DEL", Some("?")) => Kind::Del(None),
        _ => return None,
    };
    Some(Op {
        client: w[0].parse().ok()?,
        start: w[1].parse().ok()?,
        end,
        key: w[3].to_string(),
        kind,
    })
}

/// The register's next value if `op` can take effect now with the result it returned.
fn step(value: &Option<String>, op: &Op) -> Option<Option<String>> {
    match &op.kind {
        Kind::Set(v) => Some(Some(v.clone())),
        Kind::Get(read) => (read == value).then(|| value.clone()),
        Kind::Del(found) => match found {
            Some(f) if *f != value.is_some() => None,
            _ => Some(None),
        },
    }
}

fn search(
    ops: &[Op],
    left: &mut Vec<bool>,
    value: Option<String>,
    seen: &mut HashSet<(Vec<bool>, Option<String>)>,
) -> bool {
    // Done when every operation left lacks a reply: those may never have happened.
    if ops.iter().zip(left.iter()).all(|(op, &l)| !l || op.end.is_none()) {
        return true;
    }
    if !seen.insert((left.clone(), value.clone())) {
        return false; // this state was already explored and refuted
    }
    let first_end =
        (0..ops.len()).filter(|&i| left[i]).filter_map(|i| ops[i].end).min();
    for i in 0..ops.len() {
        if !left[i] || ops[i].start > first_end.unwrap() {
            continue; // done, or began after an operation that has ended
        }
        if let Some(next) = step(&value, &ops[i]) {
            left[i] = false;
            let found = search(ops, left, next, seen);
            left[i] = true;
            if found {
                return true;
            }
        }
    }
    false
}

/// For each key, whether its operations have a linearisation (the register starts empty).
pub fn check(history: &[Op]) -> BTreeMap<String, bool> {
    let mut by_key: BTreeMap<String, Vec<Op>> = BTreeMap::new();
    for op in history {
        if op.end.is_none() && matches!(op.kind, Kind::Get(_)) {
            continue; // a read without a reply changes nothing
        }
        by_key.entry(op.key.clone()).or_default().push(op.clone());
    }
    by_key
        .into_iter()
        .map(|(key, ops)| {
            let mut left = vec![true; ops.len()];
            (key, search(&ops, &mut left, None, &mut HashSet::new()))
        })
        .collect()
}
