// ex6_prec.rs -- exercise 6: resolve SLR shift-reduce conflicts by operator
// precedence and associativity, as parser generators do.
#![allow(dead_code)]
use crate::grammar::Grammar;
use crate::lr0;
use crate::slr::{self, Action, Table};

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Assoc { Left, Right, Non }

/// Operator precedences, higher binds tighter.
pub struct Prec(pub Vec<(&'static str, u8, Assoc)>);

impl Prec {
    fn of(&self, t: &str) -> Option<(u8, Assoc)> {
        self.0.iter().find(|(x, _, _)| *x == t).map(|&(_, p, a)| (p, a))
    }
    /// A rule's precedence is that of its last terminal.
    fn rule(&self, g: &Grammar, r: usize) -> Option<(u8, Assoc)> {
        g.rules[r].1.iter().rev().find(|s| !g.is_nt(s)).and_then(|s| self.of(s))
    }
}

/// The SLR table with every shift-reduce conflict between a rule and a
/// token that both have a precedence resolved; other conflicts stay.
pub fn table(g: &Grammar, prec: &Prec) -> Table {
    let mut t = slr::table(g, &lr0::automaton(g));
    for ((_, x), acts) in t.action.iter_mut() {
        if acts.len() != 2 {
            continue;
        }
        let (Action::Shift(_), Action::Reduce(r)) = (acts[0], acts[1]) else { continue };
        let (Some((pt, _)), Some((pr, assoc))) = (prec.of(x), prec.rule(g, r)) else { continue };
        if pt > pr || pt == pr && assoc == Assoc::Right {
            acts.truncate(1);
        } else if pt < pr || assoc == Assoc::Left {
            acts.remove(0);
        } else {
            acts.clear(); // non-associative: an error
        }
    }
    t.action.retain(|_, v| !v.is_empty());
    t
}

/// Parse with values: the tree of `E -> E op E` as `(op a b)`.
pub fn tree(g: &Grammar, t: &Table, input: &[&str]) -> Result<String, String> {
    let (mut st, mut val, mut i) = (vec![0usize], Vec::<String>::new(), 0);
    loop {
        let s = *st.last().unwrap();
        match t.action.get(&(s, input[i].to_string())).map(|v| v[0]) {
            Some(Action::Shift(j)) => {
                st.push(j);
                val.push(input[i].to_string());
                i += 1;
            }
            Some(Action::Reduce(r)) => {
                let (lhs, rhs) = &g.rules[r];
                let v = val.split_off(val.len() - rhs.len());
                st.truncate(st.len() - rhs.len());
                val.push(match v.len() {
                    3 if v[0] == "(" => v[1].clone(),
                    3 => format!("({} {} {})", v[1], v[0], v[2]),
                    _ => v[0].clone(),
                });
                st.push(t.goto[&(*st.last().unwrap(), lhs.clone())]);
            }
            Some(Action::Accept) => return Ok(val.pop().unwrap()),
            None => return Err(format!("error at token {} ({})", i + 1, input[i])),
        }
    }
}
