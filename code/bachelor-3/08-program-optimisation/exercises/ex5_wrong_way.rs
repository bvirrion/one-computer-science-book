// ex5_wrong_way.rs -- exercise 5: liveness with the facts flowing forward.
// The transfer function is the right one; the direction is not.
#![allow(dead_code)]
use crate::cfg::Cfg;
use crate::dataflow::{Analysis, Dir};
use crate::liveness::{step, Set};
use crate::tac::Tac;

pub struct WrongWay<'a> {
    pub code: &'a [Tac],
    pub g: &'a Cfg,
}

impl Analysis for WrongWay<'_> {
    type V = Set;
    fn dir(&self) -> Dir { Dir::Forward } // the bug
    fn bottom(&self) -> Set { Set::new() }
    fn boundary(&self) -> Set { Set::new() }
    fn join(&self, a: &Set, b: &Set) -> Set { a.union(b).copied().collect() }
    fn transfer(&self, b: usize, x: &Set) -> Set {
        let (s, e) = self.g.blocks[b];
        self.code[s..e]
            .iter()
            .rev()
            .fold(x.clone(), |live, i| step(i, &live))
    }
}
