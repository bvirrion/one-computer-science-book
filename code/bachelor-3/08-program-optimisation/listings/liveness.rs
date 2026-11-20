// liveness.rs -- live temporaries: a backward analysis on sets, joined by union.
#![allow(dead_code)]
use crate::cfg::Cfg;
use crate::dataflow::{Analysis, Dir};
use crate::tac::{Tac, Val};
use std::collections::BTreeSet;

pub type Set = BTreeSet<u32>;

/// The temporaries an instruction reads.
pub fn uses(i: &Tac) -> Vec<u32> {
    let vals: Vec<Val> = match i {
        Tac::Bin(_, _, a, b) | Tac::Branch(_, a, b, _) | Tac::StoreA(_, a, b) => vec![*a, *b],
        Tac::Neg(_, a) | Tac::Not(_, a) | Tac::Copy(_, a) | Tac::StoreG(_, a) => vec![*a],
        Tac::LoadA(_, _, a) | Tac::Ret(Some(a)) => vec![*a],
        Tac::Call(_, _, args) => args.clone(),
        _ => vec![],
    };
    vals.into_iter()
        .filter_map(|v| if let Val::T(t) = v { Some(t) } else { None })
        .collect()
}

/// The temporary an instruction writes, if any.
pub fn def(i: &Tac) -> Option<u32> {
    match i {
        Tac::Bin(d, ..) | Tac::Neg(d, _) | Tac::Not(d, _) | Tac::Copy(d, _) => Some(*d),
        Tac::LoadG(d, _) | Tac::LoadA(d, ..) => Some(*d),
        Tac::Call(d, ..) => *d,
        _ => None,
    }
}

/// live before i = uses(i) + (live after i - def(i))
pub fn step(i: &Tac, after: &Set) -> Set {
    let mut s = after.clone();
    if let Some(d) = def(i) {
        s.remove(&d);
    }
    s.extend(uses(i));
    s
}

pub struct Liveness<'a> {
    pub code: &'a [Tac],
    pub g: &'a Cfg,
}

impl Analysis for Liveness<'_> {
    type V = Set;
    fn dir(&self) -> Dir { Dir::Backward }
    fn bottom(&self) -> Set { Set::new() }
    fn boundary(&self) -> Set { Set::new() } // nothing is live after a return
    fn join(&self, a: &Set, b: &Set) -> Set { a.union(b).copied().collect() }
    fn transfer(&self, b: usize, out: &Set) -> Set {
        let (s, e) = self.g.blocks[b];
        self.code[s..e].iter().rev().fold(out.clone(), |live, i| step(i, &live))
    }
}

/// The live set after every instruction, from the block solution.
pub fn live_after(code: &[Tac], g: &Cfg, after_block: &[Set]) -> Vec<Set> {
    let mut res = vec![Set::new(); code.len()];
    for (b, &(s, e)) in g.blocks.iter().enumerate() {
        let mut live = after_block[b].clone();
        for k in (s..e).rev() {
            res[k] = live.clone();
            live = step(&code[k], &live);
        }
    }
    res
}
