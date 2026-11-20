// count.rs: the number of parse trees of a word, by dynamic programming on its spans.
use crate::grammar::{Grammar, Sym};
use std::collections::{HashMap, HashSet};

struct Counter<'a> {
    g: &'a Grammar,
    w: Vec<char>,
    null: HashSet<String>,
    memo: HashMap<(String, usize, usize), Option<u128>>, // None: being computed
}

/// The parse trees of `word` from the start symbol. The grammar must not allow A =>+ A
/// for a nonterminal A, which would give infinitely many trees.
pub fn trees(g: &Grammar, word: &str) -> u128 {
    let w: Vec<char> = word.chars().collect();
    let n = w.len();
    let mut c = Counter { g, w, null: g.nullable(), memo: HashMap::new() };
    c.span(&g.start, 0, n)
}

impl Counter<'_> {
    /// The trees of w[i..j] with root a: the sum over a's rules.
    fn span(&mut self, a: &str, i: usize, j: usize) -> u128 {
        let key = (a.to_string(), i, j);
        if let Some(known) = self.memo.get(&key) {
            return known.expect("A =>+ A: infinitely many trees");
        }
        self.memo.insert(key.clone(), None);
        let mut total = 0;
        for (b, rhs) in &self.g.rules {
            if b == a {
                total += self.seq(rhs, i, j);
            }
        }
        self.memo.insert(key, Some(total));
        total
    }

    /// The ways for the symbols of `rhs` to derive w[i..j], each taking a consecutive part.
    fn seq(&mut self, rhs: &[Sym], i: usize, j: usize) -> u128 {
        match rhs.split_first() {
            None => (i == j) as u128,
            Some((Sym::T(c), rest)) if i < j && self.w[i] == *c => self.seq(rest, i + 1, j),
            Some((Sym::T(_), _)) => 0,
            Some((Sym::N(b), rest)) => {
                // the rest needs a letter for each of its symbols that cannot vanish
                let solid = rest.iter()
                    .filter(|s| !matches!(s, Sym::N(x) if self.null.contains(x))).count();
                let first = if self.null.contains(b) { i } else { i + 1 }; // b's letters too
                let mut ways = 0;
                for k in first..(j + 1).saturating_sub(solid) { // b takes w[i..k]
                    let left = self.span(b, i, k);
                    if left > 0 {
                        ways += left * self.seq(rest, k, j);
                    }
                }
                ways
            }
        }
    }
}
