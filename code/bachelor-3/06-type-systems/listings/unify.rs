// unify.rs -- substitutions on types, and unification with the occurs
// check: the most general substitution that makes two types equal.
#![allow(dead_code)]
use crate::lam::{show_ty, Ty};
use std::collections::{BTreeMap, BTreeSet};
use std::sync::atomic::{AtomicUsize, Ordering};

pub type Subst = BTreeMap<u32, Ty>;
pub static UNIFY_CALLS: AtomicUsize = AtomicUsize::new(0);

/// s(t): every variable bound by s replaced (s is kept idempotent).
pub fn apply(s: &Subst, t: &Ty) -> Ty {
    match t {
        Ty::Var(a) => s.get(a).cloned().unwrap_or(Ty::Var(*a)),
        Ty::Fun(a, b) => Ty::Fun(Box::new(apply(s, a)), Box::new(apply(s, b))),
        Ty::Pair(a, b) => Ty::Pair(Box::new(apply(s, a)), Box::new(apply(s, b))),
        Ty::Int | Ty::Bool => t.clone(),
    }
}

pub fn type_vars(t: &Ty, out: &mut BTreeSet<u32>) {
    match t {
        Ty::Var(a) => { out.insert(*a); }
        Ty::Fun(a, b) | Ty::Pair(a, b) => { type_vars(a, out); type_vars(b, out); }
        Ty::Int | Ty::Bool => {}
    }
}

pub fn occurs(a: u32, t: &Ty) -> bool {
    let mut vs = BTreeSet::new();
    type_vars(t, &mut vs);
    vs.contains(&a)
}

/// Add a := t to s, t being already s-applied; s stays idempotent.
fn bind(s: &mut Subst, a: u32, t: Ty) -> Result<(), String> {
    if t == Ty::Var(a) {
        return Ok(());
    }
    if occurs(a, &t) {
        return Err(format!("{} would have to equal {}, which contains it",
                           show_ty(&Ty::Var(a)), show_ty(&t)));
    }
    let one = Subst::from([(a, t.clone())]);
    for u in s.values_mut() {
        *u = apply(&one, u);
    }
    s.insert(a, t);
    Ok(())
}

/// Extend s so that s(t1) = s(t2), as generally as possible.
pub fn unify(s: &mut Subst, t1: &Ty, t2: &Ty) -> Result<(), String> {
    UNIFY_CALLS.fetch_add(1, Ordering::Relaxed);
    let (a, b) = (apply(s, t1), apply(s, t2));
    match (&a, &b) {
        (Ty::Var(x), _) => bind(s, *x, b.clone()),
        (_, Ty::Var(y)) => bind(s, *y, a.clone()),
        (Ty::Int, Ty::Int) | (Ty::Bool, Ty::Bool) => Ok(()),
        (Ty::Fun(a1, r1), Ty::Fun(a2, r2)) | (Ty::Pair(a1, r1), Ty::Pair(a2, r2)) => {
            unify(s, a1, a2)?;
            unify(s, r1, r2)
        }
        _ => Err(format!("{} is not {}", show_ty(&a), show_ty(&b))),
    }
}

/// Rename the variables of t to 'a, 'b, ... in order of first appearance.
pub fn normalise(t: &Ty) -> Ty {
    fn go(t: &Ty, names: &mut Vec<u32>) -> Ty {
        match t {
            Ty::Var(a) => {
                let k = names.iter().position(|x| x == a).unwrap_or_else(|| {
                    names.push(*a);
                    names.len() - 1
                });
                Ty::Var(k as u32)
            }
            Ty::Fun(a, b) => Ty::Fun(Box::new(go(a, names)), Box::new(go(b, names))),
            Ty::Pair(a, b) => Ty::Pair(Box::new(go(a, names)), Box::new(go(b, names))),
            Ty::Int | Ty::Bool => t.clone(),
        }
    }
    go(t, &mut vec![])
}
