// ex5_noocc.rs -- exercise 5: unification on a triangular substitution
// (a := t, where t may mention other bound variables), with and without
// the occurs check.
#![allow(dead_code)]
use crate::lam::Ty;
use std::collections::BTreeMap;

pub type Tri = BTreeMap<u32, Ty>;

/// Follow bindings to the end, or None once `fuel` nodes are spent.
pub fn resolve(s: &Tri, t: &Ty, fuel: &mut usize) -> Option<Ty> {
    if *fuel == 0 {
        return None;
    }
    *fuel -= 1;
    Some(match t {
        Ty::Var(a) => match s.get(a) {
            Some(u) => return resolve(s, u, fuel),
            None => t.clone(),
        },
        Ty::Fun(a, b) => Ty::Fun(Box::new(resolve(s, a, fuel)?), Box::new(resolve(s, b, fuel)?)),
        Ty::Pair(a, b) => Ty::Pair(Box::new(resolve(s, a, fuel)?), Box::new(resolve(s, b, fuel)?)),
        _ => t.clone(),
    })
}

fn walk(s: &Tri, t: &Ty) -> Ty {
    match t {
        Ty::Var(a) if s.contains_key(a) => walk(s, &s[a]),
        _ => t.clone(),
    }
}

/// Does a occur in t, once t is resolved? (Safe: s has no cycle so far.)
fn occurs(s: &Tri, a: u32, t: &Ty) -> bool {
    match walk(s, t) {
        Ty::Var(b) => a == b,
        Ty::Fun(x, y) | Ty::Pair(x, y) => occurs(s, a, &x) || occurs(s, a, &y),
        _ => false,
    }
}

pub fn unify(s: &mut Tri, a: &Ty, b: &Ty, occurs_check: bool) -> Result<(), String> {
    let (a, b) = (walk(s, a), walk(s, b));
    match (&a, &b) {
        (Ty::Var(x), Ty::Var(y)) if x == y => Ok(()),
        (Ty::Var(x), t) | (t, Ty::Var(x)) => {
            if occurs_check && occurs(s, *x, t) {
                return Err("infinite type".into());
            }
            s.insert(*x, t.clone());
            Ok(())
        }
        (Ty::Int, Ty::Int) | (Ty::Bool, Ty::Bool) => Ok(()),
        (Ty::Fun(a1, r1), Ty::Fun(a2, r2)) | (Ty::Pair(a1, r1), Ty::Pair(a2, r2)) => {
            unify(s, a1, a2, occurs_check)?;
            unify(s, r1, r2, occurs_check)
        }
        _ => Err("mismatch".into()),
    }
}
