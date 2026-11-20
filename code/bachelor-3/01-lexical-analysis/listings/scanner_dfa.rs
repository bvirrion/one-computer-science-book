// scanner_dfa.rs -- the subset construction with priorities, minimisation,
// and the longest-match scanner that runs the table.
#![allow(dead_code)]
use crate::regex_nfa::Nfa;
use std::collections::{BTreeSet, HashMap};

pub const DEAD: usize = usize::MAX;

/// A scanner DFA as a table: one row per state, one column per ASCII byte.
pub struct Dfa {
    pub next: Vec<[usize; 128]>,  // DEAD where the row has no move
    pub accept: Vec<Option<usize>>, // the token class a state accepts
    pub nfa_sets: Vec<Vec<usize>>,  // what each state stands for (before minimising)
}

fn closure(nfa: &Nfa, set: &mut BTreeSet<usize>) {
    let mut stack: Vec<usize> = set.iter().copied().collect();
    while let Some(s) = stack.pop() {
        for &t in &nfa.states[s].eps {
            if set.insert(t) {
                stack.push(t);
            }
        }
    }
}

/// The subset construction. A DFA state accepts the rule of smallest
/// index among the NFA states it contains: the rule written first wins.
pub fn subset(nfa: &Nfa) -> Dfa {
    let mut first = BTreeSet::from([nfa.start]);
    closure(nfa, &mut first);
    let mut index: HashMap<BTreeSet<usize>, usize> = HashMap::from([(first.clone(), 0)]);
    let mut sets = vec![first];
    let mut dfa = Dfa { next: Vec::new(), accept: Vec::new(), nfa_sets: Vec::new() };
    let mut k = 0;
    while k < sets.len() {
        let mut row = [DEAD; 128];
        for (c, cell) in row.iter_mut().enumerate() {
            let mut target = BTreeSet::new();
            for &s in &sets[k] {
                for &(lo, hi, t) in &nfa.states[s].moves {
                    if lo as usize <= c && c <= hi as usize {
                        target.insert(t);
                    }
                }
            }
            if target.is_empty() {
                continue;
            }
            closure(nfa, &mut target);
            let n = sets.len();
            *cell = *index.entry(target.clone()).or_insert_with(|| {
                sets.push(target);
                n
            });
        }
        let rule = sets[k].iter().filter_map(|&s| nfa.states[s].accept).min();
        dfa.next.push(row);
        dfa.accept.push(rule);
        dfa.nfa_sets.push(sets[k].iter().copied().collect());
        k += 1;
    }
    dfa
}

/// Moore's minimisation. The first partition puts states together only if
/// they accept the same rule: two token classes are never merged.
pub fn minimise(d: &Dfa) -> Dfa {
    let n = d.next.len();
    let mut block: Vec<usize> = d.accept.iter().map(|a| a.map_or(0, |r| r + 1)).collect();
    loop {
        // a state's signature: its block and the block each byte leads to
        let sig = |s: usize, block: &[usize]| -> Vec<usize> {
            let mut v = vec![block[s]];
            v.extend(d.next[s].iter().map(|&t| if t == DEAD { DEAD } else { block[t] }));
            v
        };
        let mut ids: HashMap<Vec<usize>, usize> = HashMap::new();
        let mut order = Vec::new(); // blocks numbered by first appearance: state 0 stays 0
        let new: Vec<usize> = (0..n)
            .map(|s| {
                let k = ids.len();
                *ids.entry(sig(s, &block)).or_insert_with(|| {
                    order.push(s);
                    k
                })
            })
            .collect();
        let stable = ids.len() == block.iter().collect::<BTreeSet<_>>().len();
        block = new;
        if stable {
            let next = order
                .iter()
                .map(|&s| d.next[s].map(|t| if t == DEAD { DEAD } else { block[t] }))
                .collect();
            let accept = order.iter().map(|&s| d.accept[s]).collect();
            let nfa_sets = order.iter().map(|&s| d.nfa_sets[s].clone()).collect();
            return Dfa { next, accept, nfa_sets };
        }
    }
}

/// The longest match from `from`: the end and class of the longest token,
/// and how many characters the DFA read to find it (the backtracked ones too).
pub fn longest(d: &Dfa, input: &[u8], from: usize) -> (Option<(usize, usize)>, usize) {
    let (mut state, mut pos, mut last) = (0, from, None);
    while pos < input.len() && input[pos] < 128 {
        state = d.next[state][input[pos] as usize];
        if state == DEAD {
            break;
        }
        pos += 1;
        if let Some(rule) = d.accept[state] {
            last = Some((pos, rule));
        }
    }
    (last, pos - from + usize::from(state == DEAD))
}

/// Maximal munch over the whole input: (class, start, end) for each token,
/// and the total number of characters read; Err(position) where no rule matches.
pub fn scan(d: &Dfa, input: &[u8]) -> Result<(Vec<(usize, usize, usize)>, usize), usize> {
    let (mut out, mut pos, mut reads) = (Vec::new(), 0, 0);
    while pos < input.len() {
        let (m, r) = longest(d, input, pos);
        reads += r;
        let (end, rule) = m.ok_or(pos)?;
        out.push((rule, pos, end));
        pos = end;
    }
    Ok((out, reads))
}
