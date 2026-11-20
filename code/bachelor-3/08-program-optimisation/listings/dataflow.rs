// dataflow.rs -- a dataflow analysis is a least fixed point, computed by a
// worklist over the blocks of a control-flow graph.
#![allow(dead_code)]
use crate::cfg::Cfg;
use std::collections::VecDeque;

#[derive(Clone, Copy, PartialEq)]
pub enum Dir {
    Forward,
    Backward,
}

/// A monotone framework: a lattice of facts and a transfer function per block.
pub trait Analysis {
    type V: Clone + PartialEq;
    fn dir(&self) -> Dir;
    fn bottom(&self) -> Self::V; // the starting value of every block
    fn boundary(&self) -> Self::V; // the fact at the entry (forward) or an exit (backward)
    fn join(&self, a: &Self::V, b: &Self::V) -> Self::V;
    fn transfer(&self, block: usize, x: &Self::V) -> Self::V;
}

/// Facts before and after each block, in program order, and the visits made.
pub struct Solution<V> {
    pub before: Vec<V>,
    pub after: Vec<V>,
    pub visits: usize,
}

pub fn preds(g: &Cfg) -> Vec<Vec<usize>> {
    let mut p = vec![vec![]; g.blocks.len()];
    for (b, ss) in g.succ.iter().enumerate() {
        for &s in ss {
            p[s].push(b);
        }
    }
    p
}

pub fn solve<A: Analysis>(a: &A, g: &Cfg) -> Solution<A::V> {
    let (n, p, dir) = (g.blocks.len(), preds(g), a.dir());
    // inn: the side facts flow in from; out: the side the transfer produces
    let (mut inn, mut out) = (vec![a.bottom(); n], vec![a.bottom(); n]);
    let mut work: VecDeque<usize> = (0..n).collect();
    let mut queued = vec![true; n];
    let mut visits = 0;
    while let Some(b) = work.pop_front() {
        queued[b] = false;
        visits += 1;
        let (from, to) = match dir {
            Dir::Forward => (&p[b], &g.succ[b]),
            Dir::Backward => (&g.succ[b], &p[b]),
        };
        let at_boundary = if dir == Dir::Forward { b == 0 } else { g.succ[b].is_empty() };
        let mut x = if at_boundary { a.boundary() } else { a.bottom() };
        for &s in from {
            x = a.join(&x, &out[s]);
        }
        let y = a.transfer(b, &x);
        inn[b] = x;
        if y != out[b] {
            out[b] = y;
            for &m in to {
                if !queued[m] {
                    queued[m] = true;
                    work.push_back(m);
                }
            }
        }
    }
    match dir {
        Dir::Forward => Solution { before: inn, after: out, visits },
        Dir::Backward => Solution { before: out, after: inn, visits },
    }
}
