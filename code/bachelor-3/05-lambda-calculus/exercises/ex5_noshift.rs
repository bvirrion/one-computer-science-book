// ex5_noshift.rs -- the bug of exercise 5: substitution that forgets to
// shift the substituted term under a λ.
#![allow(dead_code)]
use crate::reduce::shift;
use crate::term::{Term, Term::*};

pub fn subst_noshift(j: usize, s: &Term, t: &Term) -> Term {
    match t {
        Var(k) if *k == j => s.clone(),
        Var(k) => Var(*k),
        Free(x) => Free(x.clone()),
        Lam(x, b) => Lam(x.clone(), Box::new(subst_noshift(j + 1, s, b))), // the bug
        App(f, a) => App(Box::new(subst_noshift(j, s, f)), Box::new(subst_noshift(j, s, a))),
    }
}

pub fn beta_noshift(body: &Term, arg: &Term) -> Term {
    shift(-1, 0, &subst_noshift(0, &shift(1, 0, arg), body))
}
