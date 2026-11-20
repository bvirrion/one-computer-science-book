// dict_bugs.rs: the three bugs of dict.c, written in Rust; build with --cfg bug1, bug2 or bug3.
#![allow(unexpected_cfgs)]
mod dict_table;
use dict_table::Dict;
#[allow(unused_imports)]
use std::collections::HashMap;

#[cfg(bug1)]
fn bug(d: &mut Dict, w: &str) {
    let first = d.count("The"); // a reference into the table, kept...
    *d.count(w) += 1; // ...across an insertion that may move the slots
    *first += 0;
}

#[cfg(bug2)]
fn bug(d: &mut Dict, _w: &str) {
    let best: &String = d.iter().next().unwrap().0; // borrowed from the table
    let mine: String = *best; // take the word for ourselves, to free it
    drop(mine);
}

#[cfg(bug3)]
fn bug(_d: &mut Dict, _w: &str) {
    let mut counts: HashMap<&str, u32> = HashMap::new(); // keeps the caller's words, not copies
    for i in 0..2 {
        let line = format!("line {i}"); // a buffer that dies at the end of each iteration
        for w in line.split(' ') {
            *counts.entry(w).or_insert(0) += 1;
        }
    }
    println!("{}", counts.len());
}

fn main() {
    let mut d = Dict::default();
    bug(&mut d, "Mill");
}
