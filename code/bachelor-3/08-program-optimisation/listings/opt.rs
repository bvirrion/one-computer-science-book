// opt.rs -- the classic optimisations on three-address code: constant
// propagation and folding, copy propagation, local value numbering, and
// dead-code elimination, repeated until nothing changes.
#![allow(dead_code)]
use crate::ast::BinOp;
use crate::cfg::{self, Cfg};
use crate::dataflow::{solve, Analysis, Dir};
use crate::liveness::{def, live_after, Liveness};
use crate::ssa::reachable;
use crate::tac::{FuncTac, Tac, Val};
use std::collections::{BTreeMap, BTreeSet};

// ---- constant propagation ----------------------------------------------------

/// The value lattice of one temporary: Undef < Const(k) < Nac (not a constant).
#[derive(Clone, Copy, PartialEq, Debug)]
pub enum Cv {
    Undef,
    Const(i32),
    Nac,
}

pub fn meet(a: Cv, b: Cv) -> Cv {
    match (a, b) {
        (Cv::Undef, x) | (x, Cv::Undef) => x,
        (Cv::Const(x), Cv::Const(y)) if x == y => a,
        _ => Cv::Nac,
    }
}

/// Moor's arithmetic on 32-bit words, as the interpreter and the processor do it.
pub fn fold(op: BinOp, a: i32, b: i32) -> i32 {
    use BinOp::*;
    match op {
        Add => a.wrapping_add(b),
        Sub => a.wrapping_sub(b),
        Mul => a.wrapping_mul(b),
        Div => {
            if b == 0 {
                -1
            } else {
                a.wrapping_div(b)
            }
        }
        Rem => {
            if b == 0 {
                a
            } else {
                a.wrapping_rem(b)
            }
        }
        Eq => (a == b) as i32,
        Ne => (a != b) as i32,
        Lt => (a < b) as i32,
        Le => (a <= b) as i32,
        Gt => (a > b) as i32,
        Ge => (a >= b) as i32,
        And | Or => unreachable!("jumping code"),
    }
}

pub type Env = BTreeMap<u32, Cv>; // a missing temporary is Undef

fn get(env: &Env, v: Val) -> Cv {
    match v {
        Val::K(k) => Cv::Const(k),
        Val::T(t) => *env.get(&t).unwrap_or(&Cv::Undef),
    }
}

/// The value an instruction gives its result, from the values of its operands.
pub fn eval(env: &Env, i: &Tac) -> Cv {
    let lift = |x: Cv, f: &dyn Fn(i32) -> i32| match x {
        Cv::Const(k) => Cv::Const(f(k)),
        o => o,
    };
    match i {
        Tac::Bin(_, op, a, b) => match (get(env, *a), get(env, *b)) {
            (Cv::Const(x), Cv::Const(y)) => Cv::Const(fold(*op, x, y)),
            (Cv::Undef, _) | (_, Cv::Undef) => Cv::Undef,
            _ => Cv::Nac,
        },
        Tac::Neg(_, a) => lift(get(env, *a), &|k| k.wrapping_neg()),
        Tac::Not(_, a) => lift(get(env, *a), &|k| 1 - k),
        Tac::Copy(_, a) => get(env, *a),
        _ => Cv::Nac, // a load or a call: unknown
    }
}

pub fn cp_step(env: &Env, i: &Tac) -> Env {
    let mut e = env.clone();
    if let Some(d) = def(i) {
        e.insert(d, eval(env, i));
    }
    e
}

pub struct ConstProp<'a> {
    pub f: &'a FuncTac,
    pub g: &'a Cfg,
}

impl Analysis for ConstProp<'_> {
    type V = Env;
    fn dir(&self) -> Dir { Dir::Forward }
    fn bottom(&self) -> Env { Env::new() }
    fn boundary(&self) -> Env { self.f.params.iter().map(|&p| (p, Cv::Nac)).collect() }
    fn join(&self, a: &Env, b: &Env) -> Env {
        let mut r = a.clone();
        for (&t, &v) in b {
            r.insert(t, meet(*a.get(&t).unwrap_or(&Cv::Undef), v));
        }
        r
    }
    fn transfer(&self, b: usize, x: &Env) -> Env {
        let (s, e) = self.g.blocks[b];
        self.f.code[s..e]
            .iter()
            .fold(x.clone(), |env, i| cp_step(&env, i))
    }
}

/// The instruction with each operand replaced by f(operand).
pub fn map_uses(i: &Tac, f: &mut dyn FnMut(Val) -> Val) -> Tac {
    match i {
        Tac::Bin(d, op, a, b) => Tac::Bin(*d, *op, f(*a), f(*b)),
        Tac::Neg(d, a) => Tac::Neg(*d, f(*a)),
        Tac::Not(d, a) => Tac::Not(*d, f(*a)),
        Tac::Copy(d, a) => Tac::Copy(*d, f(*a)),
        Tac::StoreG(g, a) => Tac::StoreG(g.clone(), f(*a)),
        Tac::LoadA(d, arr, a) => Tac::LoadA(*d, arr.clone(), f(*a)),
        Tac::StoreA(arr, a, b) => Tac::StoreA(arr.clone(), f(*a), f(*b)),
        Tac::Branch(op, a, b, l) => Tac::Branch(*op, f(*a), f(*b), *l),
        Tac::Call(d, g, args) => Tac::Call(*d, g.clone(), args.iter().map(|a| f(*a)).collect()),
        Tac::Ret(Some(a)) => Tac::Ret(Some(f(*a))),
        other => other.clone(),
    }
}

/// Uses replaced by known constants, constant operations folded, and branches
/// whose outcome is known replaced by a jump or removed.
pub fn const_prop(f: &mut FuncTac) -> usize {
    let g = cfg::build(f);
    let sol = solve(&ConstProp { f, g: &g }, &g);
    let mut out: Vec<Tac> = vec![];
    for (b, &(s, e)) in g.blocks.iter().enumerate() {
        let mut env = sol.before[b].clone();
        for i in &f.code[s..e] {
            let mut known = |v: Val| match v {
                Val::T(t) => match env.get(&t) {
                    Some(Cv::Const(c)) => Val::K(*c),
                    _ => v,
                },
                k => k,
            };
            let new = match map_uses(i, &mut known) {
                Tac::Bin(d, op, Val::K(x), Val::K(y)) => {
                    Some(Tac::Copy(d, Val::K(fold(op, x, y))))
                }
                Tac::Neg(d, Val::K(x)) => Some(Tac::Copy(d, Val::K(x.wrapping_neg()))),
                Tac::Not(d, Val::K(x)) => Some(Tac::Copy(d, Val::K(1 - x))),
                Tac::Branch(op, Val::K(x), Val::K(y), l) => {
                    (fold(op, x, y) != 0).then_some(Tac::Jump(l))
                }
                other => Some(other),
            };
            env = cp_step(&env, i);
            out.extend(new);
        }
    }
    replace(f, out)
}

fn replace(f: &mut FuncTac, code: Vec<Tac>) -> usize {
    let changed = (code != f.code) as usize;
    f.code = code;
    changed
}

// ---- copy propagation --------------------------------------------------------

/// Available copies: pairs (x, v) such that x == v holds on every path here.
/// None stands for "all pairs", the top of this must-analysis.
pub type Copies = Option<BTreeSet<(u32, Val)>>;

fn copy_step(c: &Copies, i: &Tac) -> Copies {
    let mut set = c.clone()?;
    if let Some(d) = def(i) {
        set.retain(|&(x, v)| x != d && v != Val::T(d));
        if let Tac::Copy(_, v) = i {
            if *v != Val::T(d) {
                set.insert((d, *v));
            }
        }
    }
    Some(set)
}

struct CopyProp<'a> {
    f: &'a FuncTac,
    g: &'a Cfg,
}

impl Analysis for CopyProp<'_> {
    type V = Copies;
    fn dir(&self) -> Dir { Dir::Forward }
    fn bottom(&self) -> Copies { None }
    fn boundary(&self) -> Copies { Some(BTreeSet::new()) }
    fn join(&self, a: &Copies, b: &Copies) -> Copies {
        match (a, b) {
            (None, x) | (x, None) => x.clone(),
            (Some(x), Some(y)) => Some(x.intersection(y).copied().collect()),
        }
    }
    fn transfer(&self, b: usize, x: &Copies) -> Copies {
        let (s, e) = self.g.blocks[b];
        self.f.code[s..e]
            .iter()
            .fold(x.clone(), |c, i| copy_step(&c, i))
    }
}

pub fn copy_prop(f: &mut FuncTac) -> usize {
    let g = cfg::build(f);
    let sol = solve(&CopyProp { f, g: &g }, &g);
    let mut out = vec![];
    for (b, &(s, e)) in g.blocks.iter().enumerate() {
        let mut c = sol.before[b].clone();
        for i in &f.code[s..e] {
            let set = c.clone().unwrap_or_default();
            out.push(map_uses(
                i,
                &mut |v| match set.iter().find(|(x, _)| Val::T(*x) == v) {
                    Some(&(_, w)) => w,
                    None => v,
                },
            ));
            c = copy_step(&c, i);
        }
    }
    replace(f, out)
}

// ---- local value numbering -----------------------------------------------------

fn commutes(op: BinOp) -> bool {
    matches!(op, BinOp::Add | BinOp::Mul | BinOp::Eq | BinOp::Ne)
}

/// Within each block: an operation already computed, on operands that have
/// not changed since, is replaced by a copy of the temporary that holds it.
pub fn value_number(f: &mut FuncTac) -> usize {
    let g = cfg::build(f);
    let mut out = f.code.clone();
    for &(s, e) in &g.blocks {
        let mut table: Vec<(BinOp, Val, Val, u32)> = vec![];
        for k in s..e {
            if let Tac::Bin(d, op, a, b) = out[k] {
                let (a, b) = if commutes(op) && format!("{b:?}") < format!("{a:?}") {
                    (b, a)
                } else {
                    (a, b)
                };
                if let Some(&(.., t)) = table
                    .iter()
                    .find(|&&(o, x, y, _)| o == op && x == a && y == b)
                {
                    out[k] = Tac::Copy(d, Val::T(t));
                }
                table.retain(|&(_, x, y, t)| t != d && x != Val::T(d) && y != Val::T(d));
                if a != Val::T(d) && b != Val::T(d) {
                    table.push((op, a, b, d));
                }
            } else if let Some(d) = def(&out[k]) {
                table.retain(|&(_, x, y, t)| t != d && x != Val::T(d) && y != Val::T(d));
            }
        }
    }
    replace(f, out)
}

// ---- dead code -------------------------------------------------------------------

/// Removes the blocks no path reaches, and every instruction without side
/// effect whose result is not live afterwards.
pub fn dead_code(f: &mut FuncTac) -> usize {
    let g = cfg::build(f);
    let live_blocks = reachable(&g);
    let sol = solve(&Liveness { code: &f.code, g: &g }, &g);
    let after = live_after(&f.code, &g, &sol.after);
    let mut out = vec![];
    for (b, &(s, e)) in g.blocks.iter().enumerate() {
        if !live_blocks[b] {
            continue; // unreachable: dropped whole
        }
        for k in s..e {
            let i = &f.code[k];
            let pure = matches!(i, Tac::Bin(..) | Tac::Neg(..) | Tac::Not(..) | Tac::Copy(..)
                                   | Tac::LoadG(..) | Tac::LoadA(..));
            let dead = pure && def(i).is_some_and(|d| !after[k].contains(&d));
            let self_copy = matches!(i, Tac::Copy(d, Val::T(s)) if d == s);
            let jump_to_next =
                matches!(i, Tac::Jump(l) if f.code.get(k + 1) == Some(&Tac::Label(*l)));
            if !(dead || self_copy || jump_to_next) {
                out.push(i.clone());
            }
        }
    }
    replace(f, out)
}

/// All four, in turn, until a round changes nothing; returns the rounds made.
pub fn optimise(f: &mut FuncTac) -> usize {
    let mut rounds = 0;
    loop {
        rounds += 1;
        let changed = const_prop(f) + copy_prop(f) + value_number(f) + dead_code(f);
        if changed == 0 || rounds == 20 {
            return rounds;
        }
    }
}
