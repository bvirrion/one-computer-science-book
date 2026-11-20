// ex12_lalr_prop.rs -- exercise 12: LALR look-aheads by propagation on the
// LR(0) automaton, without building the LR(1) automaton.
#![allow(dead_code)]
use crate::grammar::{self, Grammar, Set};
use crate::lr0::{self, next_sym, Item};
use std::collections::BTreeMap;

/// For each LR(0) state, the look-ahead set of each of its items.
pub fn lookaheads(g: &Grammar) -> (lr0::Lr0, Vec<BTreeMap<Item, Set>>) {
    let a = lr0::automaton(g);
    let sets = grammar::compute(g);
    let mut la: Vec<BTreeMap<Item, Set>> = a.states.iter()
        .map(|s| s.iter().map(|&it| (it, Set::new())).collect()).collect();
    la[0].get_mut(&(0, 0)).unwrap().insert("$".into());
    let mut changed = true;
    while changed {
        changed = false;
        for k in 0..a.states.len() {
            for &(r, d) in &a.states[k] {
                let here = la[k][&(r, d)].clone();
                let Some(x) = next_sym(g, (r, d)) else { continue };
                // along the transition: the same look-aheads, dot moved
                let j = a.trans[&(k, x.clone())];
                let to = la[j].get_mut(&(r, d + 1)).unwrap();
                let n = to.len();
                to.extend(here.iter().cloned());
                changed |= to.len() != n;
                // into the closure: FIRST of what follows B, and ours if nullable
                if g.is_nt(x) {
                    let (mut look, nullable) = sets.first_seq(g, &g.rules[r].1[d + 1..]);
                    if nullable {
                        look.extend(here);
                    }
                    for (r2, _) in g.rules.iter().enumerate().filter(|(_, (l, _))| l == x) {
                        let to = la[k].get_mut(&(r2, 0)).unwrap();
                        let n = to.len();
                        to.extend(look.iter().cloned());
                        changed |= to.len() != n;
                    }
                }
            }
        }
    }
    (a, la)
}
