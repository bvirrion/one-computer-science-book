// lr0.rs -- LR(0) items, their closure, the goto function and the LR(0)
// automaton of a grammar (read by ch. 2's grammar.rs).
#![allow(dead_code)]
use crate::grammar::Grammar;
use std::collections::{BTreeMap, BTreeSet};

/// An item: a rule index and the position of the dot in its right side.
pub type Item = (usize, usize);
pub type State = BTreeSet<Item>;

/// The augmented grammar: a new start rule `Start -> S` gets index 0.
pub fn augment(g: &Grammar) -> Grammar {
    let mut rules = vec![("Start".to_string(), vec![g.start().to_string()])];
    rules.extend(g.rules.iter().cloned());
    let mut nonterms = vec!["Start".to_string()];
    nonterms.extend(g.nonterms.iter().cloned());
    Grammar { rules, nonterms }
}

/// The symbol after the dot, if any.
pub fn next_sym(g: &Grammar, (r, d): Item) -> Option<&String> {
    g.rules[r].1.get(d)
}

/// Add B -> .gamma for every item with the dot before a nonterminal B,
/// until nothing changes.
pub fn closure(g: &Grammar, items: &State) -> State {
    let mut out = items.clone();
    let mut todo: Vec<Item> = items.iter().copied().collect();
    while let Some(it) = todo.pop() {
        let Some(b) = next_sym(g, it) else { continue };
        for (r, (lhs, _)) in g.rules.iter().enumerate() {
            if lhs == b && out.insert((r, 0)) {
                todo.push((r, 0));
            }
        }
    }
    out
}

/// goto(I, X): move the dot over X in every item of I that allows it.
pub fn goto(g: &Grammar, items: &State, x: &str) -> State {
    let moved: State = items.iter().filter(|&&it| next_sym(g, it).map(|s| s.as_str()) == Some(x))
        .map(|&(r, d)| (r, d + 1)).collect();
    closure(g, &moved)
}

pub struct Lr0 {
    pub states: Vec<State>,
    pub trans: BTreeMap<(usize, String), usize>,
}

/// States in order of discovery, symbols in the order their items list them.
pub fn automaton(g: &Grammar) -> Lr0 {
    let mut a = Lr0 { states: vec![closure(g, &State::from([(0, 0)]))], trans: BTreeMap::new() };
    let mut k = 0;
    while k < a.states.len() {
        let mut syms: Vec<String> = Vec::new();
        for &it in &a.states[k] {
            if let Some(s) = next_sym(g, it) {
                if !syms.contains(s) {
                    syms.push(s.clone());
                }
            }
        }
        for x in syms {
            let target = goto(g, &a.states[k], &x);
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

pub fn show_item(g: &Grammar, (r, d): Item) -> String {
    let (lhs, rhs) = &g.rules[r];
    let mut parts: Vec<&str> = rhs.iter().map(|s| s.as_str()).collect();
    parts.insert(d, ".");
    format!("{lhs} -> {}", parts.join(" "))
}
