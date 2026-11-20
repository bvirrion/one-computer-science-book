// reaching.rs -- reaching definitions: which assignments may still hold
// at each point; a forward analysis on sets of instruction numbers.
#![allow(dead_code)]
use crate::cfg::Cfg;
use crate::dataflow::{Analysis, Dir};
use crate::liveness::def;
use crate::tac::Tac;
use std::collections::BTreeSet;

pub struct Reaching<'a> {
    pub code: &'a [Tac],
    pub g: &'a Cfg,
}

impl Reaching<'_> {
    /// One instruction: its definition kills the others of the same temporary.
    pub fn step(&self, k: usize, x: &BTreeSet<usize>) -> BTreeSet<usize> {
        match def(&self.code[k]) {
            None => x.clone(),
            Some(t) => {
                let mut y: BTreeSet<usize> = x
                    .iter()
                    .copied()
                    .filter(|&j| def(&self.code[j]) != Some(t))
                    .collect();
                y.insert(k);
                y
            }
        }
    }
}

impl Analysis for Reaching<'_> {
    type V = BTreeSet<usize>;
    fn dir(&self) -> Dir { Dir::Forward }
    fn bottom(&self) -> Self::V { BTreeSet::new() }
    fn boundary(&self) -> Self::V { BTreeSet::new() } // parameters: defined before instruction 0
    fn join(&self, a: &Self::V, b: &Self::V) -> Self::V { a.union(b).copied().collect() }
    fn transfer(&self, b: usize, x: &Self::V) -> Self::V {
        let (s, e) = self.g.blocks[b];
        (s..e).fold(x.clone(), |acc, k| self.step(k, &acc))
    }
}
