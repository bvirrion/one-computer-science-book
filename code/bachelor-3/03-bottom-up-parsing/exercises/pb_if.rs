// pb_if.rs -- the weekend problem: which LR(1) states LALR merges, and the
// parse of a nested if with the conflict resolved by shifting.
#![allow(dead_code)]
use crate::grammar::Grammar;
use crate::lr1::{core, Lr1};

/// Groups of LR(1) states with the same core, for the cores held by more
/// than one state.
pub fn merged(a: &Lr1) -> Vec<Vec<usize>> {
    let mut groups: Vec<Vec<usize>> = Vec::new();
    for (k, s) in a.states.iter().enumerate() {
        match groups.iter_mut().find(|grp| core(&a.states[grp[0]]) == core(s)) {
            Some(grp) => grp.push(k),
            None => groups.push(vec![k]),
        }
    }
    groups.retain(|grp| grp.len() > 1);
    groups
}

/// The tree of a reduction sequence of the if grammar, as nested brackets.
pub fn if_tree(g: &Grammar, rules: &[usize]) -> String {
    let mut stack: Vec<String> = Vec::new();
    for &r in rules {
        let n = g.rules[r].1.iter().filter(|s| *s == "S").count();
        let kids = stack.split_off(stack.len() - n);
        stack.push(match n {
            0 => "o".into(),
            1 => format!("if({})", kids[0]),
            _ => format!("if({} else {})", kids[0], kids[1]),
        });
    }
    stack.pop().unwrap()
}
