// regalloc.rs -- register allocation by graph colouring: the interference
// graph from liveness, then simplify, spill and select.
#![allow(dead_code)]
use crate::cfg::Cfg;
use crate::dataflow::{preds, solve};
use crate::liveness::{def, live_after, uses, Liveness};
use crate::ssa::dominators;
use crate::tac::{FuncTac, Tac, Val};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Default)]
pub struct Graph {
    pub adj: BTreeMap<u32, BTreeSet<u32>>, // every temporary is a node
}

impl Graph {
    fn node(&mut self, t: u32) {
        self.adj.entry(t).or_default();
    }
    fn edge(&mut self, a: u32, b: u32) {
        if a != b {
            self.adj.entry(a).or_default().insert(b);
            self.adj.entry(b).or_default().insert(a);
        }
    }
    pub fn edges(&self) -> usize {
        self.adj.values().map(|s| s.len()).sum::<usize>() / 2
    }
}

/// Two temporaries interfere if one is written while the other is live and
/// holds a different value; the source of a copy does not interfere with its target.
pub fn interference(f: &FuncTac, g: &Cfg) -> Graph {
    let sol = solve(&Liveness { code: &f.code, g }, g);
    let after = live_after(&f.code, g, &sol.after);
    let mut gr = Graph::default();
    for (k, i) in f.code.iter().enumerate() {
        for t in uses(i) {
            gr.node(t);
        }
        if let Some(d) = def(i) {
            gr.node(d);
            for &t in &after[k] {
                if !matches!(i, Tac::Copy(_, Val::T(s)) if *s == t) {
                    gr.edge(d, t);
                }
            }
        }
    }
    let entry: BTreeSet<u32> = sol.before.first().cloned().unwrap_or_default();
    for (n, &p) in f.params.iter().enumerate() {
        // the parameters arrive together
        gr.node(p);
        for &q in f.params[..n].iter().chain(&entry) {
            gr.edge(p, q);
        }
    }
    gr
}

/// How many loops contain each block: a back edge b -> h, with h dominating b,
/// closes a loop made of h and every block that reaches b without passing h.
pub fn loop_depth(g: &Cfg) -> Vec<u32> {
    let (dom, p) = (dominators(g), preds(g));
    let mut depth = vec![0; g.blocks.len()];
    for (b, ss) in g.succ.iter().enumerate() {
        for &h in ss.iter().filter(|&&h| dom[b].contains(&h)) {
            let mut body: BTreeSet<usize> = [h, b].into();
            let mut stack = vec![b];
            while let Some(x) = stack.pop() {
                for &q in &p[x] {
                    if body.insert(q) {
                        stack.push(q);
                    }
                }
            }
            for x in body {
                depth[x] += 1;
            }
        }
    }
    depth
}

/// Spill cost: each use or definition counts 10 to the power of its loop depth.
pub fn spill_costs(f: &FuncTac, g: &Cfg) -> BTreeMap<u32, f64> {
    let depth = loop_depth(g);
    let mut cost = BTreeMap::new();
    for (b, &(s, e)) in g.blocks.iter().enumerate() {
        for i in &f.code[s..e] {
            for t in uses(i).into_iter().chain(def(i)) {
                *cost.entry(t).or_insert(0.0) += 10f64.powi(depth[b] as i32);
            }
        }
    }
    cost
}

pub struct Colouring {
    pub colour: BTreeMap<u32, usize>,
    pub spilled: BTreeSet<u32>,
}

pub fn colour(gr: &Graph, k: usize, cost: &BTreeMap<u32, f64>) -> Colouring {
    let mut left: BTreeMap<u32, BTreeSet<u32>> = gr.adj.clone();
    let (mut stack, mut spilled) = (vec![], BTreeSet::new());
    while !left.is_empty() {
        // simplify: a node of degree < k can always be coloured later
        let pick = left.iter().find(|(_, ns)| ns.len() < k).map(|(&t, _)| t);
        let t = pick.unwrap_or_else(|| {
            // spill: the cheapest per neighbour removed
            let weight = |t: &u32| cost.get(t).unwrap_or(&0.0) / left[t].len() as f64;
            let t = *left
                .keys()
                .min_by(|a, b| weight(a).total_cmp(&weight(b)))
                .unwrap();
            spilled.insert(t);
            t
        });
        for n in left.remove(&t).unwrap() {
            left.get_mut(&n).unwrap().remove(&t);
        }
        if pick.is_some() {
            stack.push(t);
        }
    }
    let mut colour = BTreeMap::new();
    while let Some(t) = stack.pop() {
        // select: the lowest colour no neighbour has
        let taken: BTreeSet<usize> = gr.adj[&t]
            .iter()
            .filter_map(|n| colour.get(n).copied())
            .collect();
        colour.insert(t, (0..).find(|c| !taken.contains(c)).unwrap());
    }
    Colouring { colour, spilled }
}
