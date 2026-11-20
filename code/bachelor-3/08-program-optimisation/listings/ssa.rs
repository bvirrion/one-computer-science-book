// ssa.rs -- dominators, dominance frontiers, and static single assignment
// form: phi-functions where definitions meet, then one name per definition.
#![allow(dead_code)]
use crate::cfg::Cfg;
use crate::dataflow::preds;
use crate::liveness::{def, uses};
use crate::tac::{show, FuncTac};
use std::collections::{BTreeMap, BTreeSet};

pub fn reachable(g: &Cfg) -> Vec<bool> {
    let mut seen = vec![false; g.blocks.len()];
    let mut stack = vec![0];
    while let Some(b) = stack.pop() {
        if !std::mem::replace(&mut seen[b], true) {
            stack.extend(&g.succ[b]);
        }
    }
    seen
}

/// Dom(b): the blocks on every path from the entry to b. Iterate
/// Dom(b) = {b} + intersection of Dom(p) over the predecessors p, from "all".
pub fn dominators(g: &Cfg) -> Vec<BTreeSet<usize>> {
    let (n, p, live) = (g.blocks.len(), preds(g), reachable(g));
    let all: BTreeSet<usize> = (0..n).filter(|&b| live[b]).collect();
    let mut dom: Vec<BTreeSet<usize>> = (0..n)
        .map(|b| {
            if b == 0 {
                [0].into()
            } else if live[b] {
                all.clone()
            } else {
                [].into()
            }
        })
        .collect();
    let mut changed = true;
    while changed {
        changed = false;
        for b in 1..n {
            if !live[b] {
                continue;
            }
            let mut d = all.clone();
            for &q in p[b].iter().filter(|&&q| live[q]) {
                d = d.intersection(&dom[q]).copied().collect();
            }
            d.insert(b);
            if d != dom[b] {
                dom[b] = d;
                changed = true;
            }
        }
    }
    dom
}

/// The immediate dominator: the strict dominator that all the others dominate.
pub fn idom(dom: &[BTreeSet<usize>]) -> Vec<Option<usize>> {
    (0..dom.len())
        .map(|b| {
            dom[b]
                .iter()
                .copied()
                .filter(|&d| d != b)
                .max_by_key(|&d| dom[d].len())
        })
        .collect()
}

/// DF(x): the blocks y such that x dominates a predecessor of y but not y strictly.
pub fn frontiers(g: &Cfg, idom: &[Option<usize>]) -> Vec<BTreeSet<usize>> {
    let (p, live) = (preds(g), reachable(g));
    let mut df = vec![BTreeSet::new(); g.blocks.len()];
    for y in (0..g.blocks.len()).filter(|&y| live[y]) {
        for &q in p[y].iter().filter(|&&q| live[q]) {
            let mut runner = Some(q);
            while let Some(r) = runner {
                if Some(r) == idom[y] {
                    break;
                }
                df[r].insert(y);
                runner = idom[r];
            }
        }
    }
    df
}

/// Where phi-functions go: the iterated frontier of the blocks that define v.
pub fn phi_blocks(defs: &BTreeSet<usize>, df: &[BTreeSet<usize>]) -> BTreeSet<usize> {
    let (mut placed, mut work): (BTreeSet<usize>, Vec<usize>) =
        (BTreeSet::new(), defs.iter().copied().collect());
    while let Some(x) = work.pop() {
        for &y in &df[x] {
            if placed.insert(y) && !defs.contains(&y) {
                work.push(y);
            }
        }
    }
    placed
}

pub struct Ssa {
    pub phis: Vec<Vec<String>>, // per block
    pub code: Vec<Vec<String>>, // per block, renamed
    pub count: usize,           // phi-functions placed
}

/// SSA form of the temporaries assigned more than once (parameters count as
/// assigned at the entry); a temporary assigned once already has one name.
pub fn to_ssa(f: &FuncTac, g: &Cfg) -> Ssa {
    let (n, dom) = (g.blocks.len(), dominators(g));
    let (id, live) = (idom(&dom), reachable(g));
    let df = frontiers(g, &id);
    let mut def_blocks: BTreeMap<u32, BTreeSet<usize>> = BTreeMap::new();
    let mut count_defs: BTreeMap<u32, usize> = BTreeMap::new();
    for &prm in &f.params {
        def_blocks.entry(prm).or_default().insert(0);
        *count_defs.entry(prm).or_default() += 1;
    }
    for (b, &(s, e)) in g.blocks.iter().enumerate().filter(|(b, _)| live[*b]) {
        for t in f.code[s..e].iter().filter_map(def) {
            def_blocks.entry(t).or_default().insert(b);
            *count_defs.entry(t).or_default() += 1;
        }
    }
    let vars: Vec<u32> = count_defs
        .iter()
        .filter(|(_, &c)| c > 1)
        .map(|(&t, _)| t)
        .collect();
    let mut phi_at: Vec<Vec<u32>> = vec![vec![]; n];
    for &v in &vars {
        for b in phi_blocks(&def_blocks[&v], &df) {
            phi_at[b].push(v);
        }
    }
    let mut r = Renamer {
        f,
        g,
        vars,
        next: BTreeMap::new(),
        stack: BTreeMap::new(),
        phi_args: phi_at
            .iter()
            .map(|vs| vec![(String::new(), vec![]); vs.len()])
            .collect(),
        out: vec![vec![]; n],
        phi_at,
        id,
    };
    for &prm in &f.params {
        if r.vars.contains(&prm) {
            r.push(prm);
        }
    }
    r.walk(0);
    let mut phis = vec![vec![]; n];
    for b in 0..n {
        for k in 0..r.phi_at[b].len() {
            let (target, args) = &r.phi_args[b][k];
            let a: Vec<String> = args.iter().map(|(p, x)| format!("B{p}: {x}")).collect();
            phis[b].push(format!("{target} = phi({})", a.join(", ")));
        }
    }
    let count = r.phi_at.iter().map(|v| v.len()).sum();
    Ssa {
        phis,
        code: r.out,
        count,
    }
}

struct Renamer<'a> {
    f: &'a FuncTac,
    g: &'a Cfg,
    vars: Vec<u32>,
    next: BTreeMap<u32, u32>,
    stack: BTreeMap<u32, Vec<String>>,
    phi_args: Vec<Vec<(String, Vec<(usize, String)>)>>,
    out: Vec<Vec<String>>,
    phi_at: Vec<Vec<u32>>,
    id: Vec<Option<usize>>,
}

impl Renamer<'_> {
    fn base(&self, v: u32) -> String {
        self.f.names.get(&v).cloned().unwrap_or(format!("t{v}"))
    }
    fn push(&mut self, v: u32) -> String {
        let k = self.next.entry(v).or_insert(0);
        let name = format!(
            "{}.{k}",
            self.f.names.get(&v).cloned().unwrap_or(format!("t{v}"))
        );
        *k += 1;
        self.stack.entry(v).or_default().push(name.clone());
        name
    }
    fn top(&self, v: u32) -> String {
        self.stack
            .get(&v)
            .and_then(|s| s.last().cloned())
            .unwrap_or(format!("{}.?", self.base(v)))
    }

    /// Rename block b, then the blocks it immediately dominates.
    fn walk(&mut self, b: usize) {
        let mark: BTreeMap<u32, usize> = self.stack.iter().map(|(&v, s)| (v, s.len())).collect();
        for (k, v) in self.phi_at[b].clone().into_iter().enumerate() {
            self.phi_args[b][k].0 = self.push(v); // the phi defines a new name first
        }
        let (s, e) = self.g.blocks[b];
        for ins in &self.f.code[s..e] {
            let mut names = self.f.names.clone();
            for u in uses(ins) {
                if self.vars.contains(&u) {
                    names.insert(u, self.top(u));
                }
            }
            let shown_uses = show(
                &FuncTac {
                    names: names.clone(),
                    ..self.shell()
                },
                ins,
            );
            let line = match def(ins) {
                Some(d) if self.vars.contains(&d) => {
                    let new = self.push(d);
                    let lhs = names.get(&d).cloned().unwrap_or(format!("t{d}"));
                    // the text before " = " is the target; rename it alone
                    format!("{new}{}", &shown_uses[lhs.len()..])
                }
                _ => shown_uses,
            };
            self.out[b].push(line);
        }
        for &sb in &self.g.succ[b].clone() {
            for (k, &v) in self.phi_at[sb].clone().iter().enumerate() {
                let x = self.top(v);
                self.phi_args[sb][k].1.push((b, x));
            }
        }
        let children: Vec<usize> = (0..self.g.blocks.len())
            .filter(|&c| self.id[c] == Some(b))
            .collect();
        for child in children {
            self.walk(child);
        }
        for (v, s) in self.stack.iter_mut() {
            s.truncate(*mark.get(v).unwrap_or(&0));
        }
    }
    fn shell(&self) -> FuncTac {
        FuncTac {
            name: self.f.name.clone(),
            params: vec![],
            code: vec![],
            temps: self.f.temps,
            names: Default::default(),
        }
    }
}
