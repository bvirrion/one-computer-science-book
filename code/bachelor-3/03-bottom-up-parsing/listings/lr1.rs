// lr1.rs -- LR(1) items and automaton; LALR by merging the LR(1) states
// that have the same LR(0) core; and the conflicts of each table.
#![allow(dead_code)]
use crate::grammar::{self, Grammar, Sets};
use crate::lr0::next_sym;
use std::collections::{BTreeMap, BTreeSet};

/// An LR(1) item: rule, dot, and the terminal expected after the rule.
pub type Item1 = (usize, usize, String);
pub type State1 = BTreeSet<Item1>;

pub fn closure1(g: &Grammar, sets: &Sets, items: &State1) -> State1 {
    let mut out = items.clone();
    let mut todo: Vec<Item1> = items.iter().cloned().collect();
    while let Some((r, d, a)) = todo.pop() {
        let Some(b) = next_sym(g, (r, d)) else { continue };
        if !g.is_nt(b) {
            continue;
        }
        let (mut look, nullable) = sets.first_seq(g, &g.rules[r].1[d + 1..]);
        if nullable {
            look.insert(a.clone());
        }
        for (r2, _) in g.rules.iter().enumerate().filter(|(_, (l, _))| l == b) {
            for x in &look {
                let it = (r2, 0, x.clone());
                if out.insert(it.clone()) {
                    todo.push(it);
                }
            }
        }
    }
    out
}

pub struct Lr1 {
    pub states: Vec<State1>,
    pub trans: BTreeMap<(usize, String), usize>,
}

pub fn automaton1(g: &Grammar) -> Lr1 {
    let sets = grammar::compute(g);
    let start = closure1(g, &sets, &State1::from([(0, 0, "$".to_string())]));
    let mut a = Lr1 { states: vec![start], trans: BTreeMap::new() };
    let mut k = 0;
    while k < a.states.len() {
        let syms: BTreeSet<String> = a.states[k].iter().filter_map(|(r, d, _)| next_sym(g, (*r, *d)).cloned()).collect();
        for x in syms {
            let moved: State1 = a.states[k].iter()
                .filter(|(r, d, _)| next_sym(g, (*r, *d)) == Some(&x))
                .map(|(r, d, l)| (*r, d + 1, l.clone())).collect();
            let target = closure1(g, &sets, &moved);
            let j = match a.states.iter().position(|s| *s == target) {
                Some(j) => j,
                None => {
                    a.states.push(target);
                    a.states.len() - 1
                }
            };
            a.trans.insert((k, x), j);
        }
        k += 1;
    }
    a
}

pub fn core(s: &State1) -> BTreeSet<(usize, usize)> {
    s.iter().map(|(r, d, _)| (*r, *d)).collect()
}

/// LALR: one state per distinct core, with the union of the look-aheads.
pub fn lalr(a: &Lr1) -> Lr1 {
    let mut cores: Vec<BTreeSet<(usize, usize)>> = Vec::new();
    let mut map = Vec::new(); // LR(1) state -> LALR state
    for s in &a.states {
        let c = core(s);
        let j = cores.iter().position(|x| *x == c).unwrap_or_else(|| {
            cores.push(c);
            cores.len() - 1
        });
        map.push(j);
    }
    let mut states = vec![State1::new(); cores.len()];
    for (k, s) in a.states.iter().enumerate() {
        states[map[k]].extend(s.iter().cloned());
    }
    let trans = a.trans.iter().map(|((k, x), j)| ((map[*k], x.clone()), map[*j])).collect();
    Lr1 { states, trans }
}

/// The number of action cells holding two or more actions.
pub fn conflicts1(g: &Grammar, a: &Lr1) -> usize {
    let mut cells: BTreeMap<(usize, String), BTreeSet<String>> = BTreeMap::new();
    for ((k, x), j) in &a.trans {
        if !g.is_nt(x) {
            cells.entry((*k, x.clone())).or_default().insert(format!("s{j}"));
        }
    }
    for (k, s) in a.states.iter().enumerate() {
        for (r, d, la) in s {
            if next_sym(g, (*r, *d)).is_none() {
                cells.entry((k, la.clone())).or_default().insert(format!("r{r}"));
            }
        }
    }
    cells.values().filter(|v| v.len() > 1).count()
}
