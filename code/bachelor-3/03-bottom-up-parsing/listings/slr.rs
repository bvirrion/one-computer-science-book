// slr.rs -- SLR action and goto tables, and the shift-reduce driver.
#![allow(dead_code)]
use crate::grammar::{self, Grammar};
use crate::lr0::{next_sym, Lr0};
use std::collections::BTreeMap;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Action {
    Shift(usize),
    Reduce(usize),
    Accept,
}

pub struct Table {
    pub action: BTreeMap<(usize, String), Vec<Action>>,
    pub goto: BTreeMap<(usize, String), usize>,
}

/// Shift on the automaton's terminal moves; reduce A -> alpha in the
/// columns of FOLLOW(A); accept on $ after Start -> S.
pub fn table(g: &Grammar, a: &Lr0) -> Table {
    let follow = grammar::compute(g).follow;
    let mut t = Table { action: BTreeMap::new(), goto: BTreeMap::new() };
    for ((from, x), &to) in &a.trans {
        if g.is_nt(x) {
            t.goto.insert((*from, x.clone()), to);
        } else {
            t.action.entry((*from, x.clone())).or_default().push(Action::Shift(to));
        }
    }
    for (k, state) in a.states.iter().enumerate() {
        for &(r, d) in state {
            if next_sym(g, (r, d)).is_some() {
                continue;
            }
            if r == 0 {
                t.action.entry((k, "$".into())).or_default().push(Action::Accept);
                continue;
            }
            for x in &follow[&g.rules[r].0] {
                t.action.entry((k, x.clone())).or_default().push(Action::Reduce(r));
            }
        }
    }
    t
}

pub fn conflicts(t: &Table) -> Vec<(&(usize, String), &Vec<Action>)> {
    t.action.iter().filter(|(_, v)| v.len() > 1).collect()
}

/// Run the shift-reduce parser; with `trace`, print one line per step.
/// Returns the rules reduced, in order: a rightmost derivation in reverse.
pub fn parse(g: &Grammar, t: &Table, input: &[&str], trace: bool) -> Result<Vec<usize>, String> {
    let mut states = vec![0usize];
    let mut symbols: Vec<String> = Vec::new();
    let mut i = 0;
    let mut reduced = Vec::new();
    loop {
        let s = *states.last().unwrap();
        let a = input[i];
        let act = t.action.get(&(s, a.to_string())).and_then(|v| v.first().copied());
        if trace {
            let stack = symbols.join(" ");
            print!("{:<5} {:<14} {:<16} ", s, stack, input[i..].join(" "));
        }
        match act {
            Some(Action::Shift(j)) => {
                if trace {
                    println!("shift {j}");
                }
                states.push(j);
                symbols.push(a.to_string());
                i += 1;
            }
            Some(Action::Reduce(r)) => {
                let (lhs, rhs) = &g.rules[r];
                for _ in rhs {
                    states.pop();
                    symbols.pop();
                }
                let top = *states.last().unwrap();
                let j = t.goto[&(top, lhs.clone())];
                if trace {
                    println!("reduce {} -> {}, goto {j}", lhs, rhs.join(" "));
                }
                states.push(j);
                symbols.push(lhs.clone());
                reduced.push(r);
            }
            Some(Action::Accept) => {
                if trace {
                    println!("accept");
                }
                return Ok(reduced);
            }
            None => {
                if trace {
                    println!("error");
                }
                return Err(format!("unexpected {a} in state {s}"));
            }
        }
    }
}
