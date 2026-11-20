// memo_munch.rs -- maximal munch in linear time: remember the (state,
// position) pairs from which no token can end, and never enter them twice.
#![allow(dead_code)]
use crate::scanner_dfa::{Dfa, DEAD};
use std::collections::HashSet;

pub fn scan_memo(d: &Dfa, input: &[u8]) -> Result<(Vec<(usize, usize, usize)>, usize), usize> {
    let mut failed: HashSet<(usize, usize)> = HashSet::new();
    let (mut out, mut pos, mut reads) = (Vec::new(), 0, 0);
    while pos < input.len() {
        let (mut state, mut p, mut last) = (0, pos, None);
        let mut visited = Vec::new();
        while p < input.len() && input[p] < 128 {
            let t = d.next[state][input[p] as usize];
            reads += 1;
            if t == DEAD {
                break;
            }
            state = t;
            p += 1;
            if failed.contains(&(state, p)) {
                break; // an earlier scan went on from here and found no token
            }
            visited.push((state, p));
            if let Some(rule) = d.accept[state] {
                last = Some((p, rule));
            }
        }
        let (end, rule) = last.ok_or(pos)?;
        for &(s, q) in &visited {
            if q > end {
                failed.insert((s, q)); // reached, but no accepting state after it
            }
        }
        out.push((rule, pos, end));
        pos = end;
    }
    Ok((out, reads))
}
