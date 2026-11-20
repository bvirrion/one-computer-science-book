// bigcount.rs: CYK counting parse trees with unbounded integers (exercise 11).
use crate::grammar::{Grammar, Sym};
use std::collections::HashMap;

/// A natural number in base 2^32, least significant limb first.
#[derive(Clone, Debug, PartialEq)]
pub struct Big(Vec<u32>);

impl Big {
    pub fn small(x: u32) -> Big {
        Big(vec![x])
    }

    pub fn is_zero(&self) -> bool {
        self.0.iter().all(|&d| d == 0)
    }

    pub fn add(&self, other: &Big) -> Big {
        let (mut out, mut carry) = (vec![], 0u64);
        for k in 0..self.0.len().max(other.0.len()) {
            let digit = |x: &Big| *x.0.get(k).unwrap_or(&0) as u64;
            let s = carry + digit(self) + digit(other);
            out.push(s as u32);
            carry = s >> 32;
        }
        out.push(carry as u32);
        Big(out).trim()
    }

    pub fn mul(&self, other: &Big) -> Big {
        let mut out = vec![0u64; self.0.len() + other.0.len() + 1];
        for (i, &x) in self.0.iter().enumerate() {
            let mut carry = 0u64;
            for (j, &y) in other.0.iter().enumerate() {
                let t = out[i + j] + x as u64 * y as u64 + carry; // < 2^64: no overflow
                out[i + j] = t & 0xffff_ffff;
                carry = t >> 32;
            }
            out[i + other.0.len()] += carry;
        }
        Big(out.into_iter().map(|d| d as u32).collect()).trim()
    }

    /// Division by a small number, with the remainder.
    pub fn div_small(&self, d: u32) -> (Big, u32) {
        let (mut out, mut rest) = (vec![0; self.0.len()], 0u64);
        for k in (0..self.0.len()).rev() {
            let cur = rest << 32 | self.0[k] as u64;
            out[k] = (cur / d as u64) as u32;
            rest = cur % d as u64;
        }
        (Big(out).trim(), rest as u32)
    }

    fn trim(mut self) -> Big {
        while self.0.len() > 1 && self.0.last() == Some(&0) {
            self.0.pop();
        }
        self
    }

    pub fn decimal(&self) -> String {
        let (mut x, mut chunks) = (self.clone(), vec![]);
        loop {
            let (q, r) = x.div_small(1_000_000_000); // nine digits at a time
            chunks.push(r);
            if q.is_zero() {
                break;
            }
            x = q;
        }
        let mut s = chunks.pop().unwrap().to_string();
        s.extend(chunks.iter().rev().map(|c| format!("{c:09}")));
        s
    }
}

/// The parse trees of `word` for a grammar in Chomsky normal form: CYK with a count per
/// nonterminal in each cell instead of a set.
pub fn trees(g: &Grammar, word: &str) -> Big {
    let w: Vec<char> = word.chars().collect();
    let n = w.len();
    let mut cell: Vec<Vec<HashMap<&str, Big>>> = vec![vec![HashMap::new(); n + 1]; n];
    for (i, &c) in w.iter().enumerate() {
        for (a, _) in g.rules.iter().filter(|(_, rhs)| rhs[..] == [Sym::T(c)]) {
            cell[i][1].insert(a, Big::small(1)); // one tree: A -> c
        }
    }
    for l in 2..=n {
        for i in 0..=n - l {
            for k in 1..l {
                for (a, rhs) in &g.rules {
                    let [Sym::N(b), Sym::N(c)] = rhs.as_slice() else { continue };
                    let x = cell[i][k].get(b.as_str()); // b on the first k letters
                    let y = cell[i + k][l - k].get(c.as_str()); // c on the rest
                    let Some((x, y)) = x.zip(y) else { continue }; // both parts must exist
                    let more = x.mul(y); // a tree for b on the left, one for c on the right
                    let total = match cell[i][l].get(a.as_str()) {
                        Some(t) => t.add(&more),
                        None => more,
                    };
                    cell[i][l].insert(a, total);
                }
            }
        }
    }
    cell[0][n].get(g.start.as_str()).cloned().unwrap_or(Big::small(0))
}
