// distinct.rs: exercise 12 without the clones: borrow, then push once the borrow has ended.
use std::collections::HashSet;

pub fn distinct(names: &[String]) -> Vec<String> {
    let mut seen: Vec<String> = Vec::new();
    for n in names {
        if !seen.contains(n) {
            // the shared borrow of `contains` ended with the call
            seen.push(n.clone());
        }
    }
    seen
}

pub fn distinct_fast(names: &[String]) -> Vec<String> {
    let mut known: HashSet<&str> = HashSet::new(); // borrows the names: no copy to test
    names.iter().filter(|n| known.insert(n.as_str())).cloned().collect()
}
