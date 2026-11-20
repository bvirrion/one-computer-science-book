// grammar.rs -- context-free grammars from text; nullable, FIRST and FOLLOW
// as least fixed points; the LL(1) table.
#![allow(dead_code)]
use std::collections::{BTreeMap, BTreeSet};

pub type Set = BTreeSet<String>;

/// Rules `A -> x y | z | eps`, one nonterminal per line, alternatives
/// separated by ` | `; a line starting with `|` continues the rule above;
/// `#` starts a comment.
/// The left side of the first rule is the start symbol.
pub struct Grammar {
    pub rules: Vec<(String, Vec<String>)>, // eps is the empty right side
    pub nonterms: Vec<String>,             // in order of first definition
}

impl Grammar {
    pub fn parse(text: &str) -> Grammar {
        let mut g = Grammar { rules: Vec::new(), nonterms: Vec::new() };
        for line in text.lines().map(|l| l.split('#').next().unwrap().trim()) {
            let (lhs, rhs) = match line.split_once("->") {
                _ if line.starts_with("| ") => (g.nonterms.last().unwrap().clone(), &line[1..]),
                Some((lhs, rhs)) => (lhs.trim().to_string(), rhs),
                None => continue,
            };
            if !g.nonterms.contains(&lhs) {
                g.nonterms.push(lhs.clone());
            }
            for alt in rhs.split(" | ") {
                let syms = alt.split_whitespace().filter(|s| *s != "eps").map(String::from).collect();
                g.rules.push((lhs.clone(), syms));
            }
        }
        g
    }
    pub fn is_nt(&self, s: &str) -> bool {
        self.nonterms.iter().any(|n| n == s)
    }
    pub fn start(&self) -> &str {
        &self.nonterms[0]
    }
}

pub struct Sets {
    pub nullable: Set,
    pub first: BTreeMap<String, Set>,
    pub follow: BTreeMap<String, Set>,
    pub rounds: (usize, usize), // passes until nothing changed: FIRST, FOLLOW
}

impl Sets {
    /// FIRST of a sequence of symbols, and whether the whole sequence is nullable.
    pub fn first_seq(&self, g: &Grammar, seq: &[String]) -> (Set, bool) {
        let mut out = Set::new();
        for s in seq {
            if !g.is_nt(s) {
                out.insert(s.clone());
                return (out, false);
            }
            out.extend(self.first[s].iter().cloned());
            if !self.nullable.contains(s) {
                return (out, false);
            }
        }
        (out, true)
    }
}

/// Start from empty sets and apply every rule until nothing changes: the
/// result is the least solution of the equations.
pub fn compute(g: &Grammar) -> Sets {
    let empty = || g.nonterms.iter().map(|n| (n.clone(), Set::new())).collect();
    let mut s = Sets { nullable: Set::new(), first: empty(), follow: empty(), rounds: (0, 0) };
    let mut changed = true;
    while changed {
        changed = false;
        s.rounds.0 += 1;
        for (a, rhs) in &g.rules {
            let (f, null) = s.first_seq(g, rhs);
            let before = s.first[a].len();
            s.first.get_mut(a).unwrap().extend(f);
            changed |= s.first[a].len() != before;
            if null && s.nullable.insert(a.clone()) {
                changed = true;
            }
        }
    }
    s.follow.get_mut(g.start()).unwrap().insert("$".into());
    changed = true;
    while changed {
        changed = false;
        s.rounds.1 += 1;
        for (a, rhs) in &g.rules {
            for (i, b) in rhs.iter().enumerate().filter(|(_, b)| g.is_nt(b)) {
                let (mut f, null) = s.first_seq(g, &rhs[i + 1..]);
                if null {
                    f.extend(s.follow[a].iter().cloned());
                }
                let before = s.follow[b].len();
                s.follow.get_mut(b).unwrap().extend(f);
                changed |= s.follow[b].len() != before;
            }
        }
    }
    s
}

/// The LL(1) table: for each (nonterminal, terminal) the rules to predict.
/// The grammar is LL(1) when no cell holds two rules.
pub fn table(g: &Grammar, s: &Sets) -> BTreeMap<(String, String), Vec<usize>> {
    let mut t: BTreeMap<(String, String), Vec<usize>> = BTreeMap::new();
    for (k, (a, rhs)) in g.rules.iter().enumerate() {
        let (mut look, null) = s.first_seq(g, rhs);
        if null {
            look.extend(s.follow[a].iter().cloned());
        }
        for x in look {
            t.entry((a.clone(), x)).or_default().push(k);
        }
    }
    t
}

pub fn show_rule(g: &Grammar, k: usize) -> String {
    let (a, rhs) = &g.rules[k];
    format!("{a} -> {}", if rhs.is_empty() { "eps".to_string() } else { rhs.join(" ") })
}
