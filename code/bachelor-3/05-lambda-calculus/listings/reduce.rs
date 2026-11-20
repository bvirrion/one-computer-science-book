// reduce.rs -- substitution on de Bruijn terms, beta-reduction, and four
// strategies that choose which redex to contract.
#![allow(dead_code)]
use crate::term::{Term, Term::*};

/// Add d to every index that points outside the term (at or above `cut`).
pub fn shift(d: isize, cut: usize, t: &Term) -> Term {
    match t {
        Var(k) if *k >= cut => Var((*k as isize + d) as usize),
        Var(k) => Var(*k),
        Free(x) => Free(x.clone()),
        Lam(x, b) => Lam(x.clone(), Box::new(shift(d, cut + 1, b))),
        App(f, a) => App(Box::new(shift(d, cut, f)), Box::new(shift(d, cut, a))),
    }
}

/// t[j := s]: under each lambda, j and the free indices of s grow by one.
pub fn subst(j: usize, s: &Term, t: &Term) -> Term {
    match t {
        Var(k) if *k == j => s.clone(),
        Var(k) => Var(*k),
        Free(x) => Free(x.clone()),
        Lam(x, b) => Lam(x.clone(), Box::new(subst(j + 1, &shift(1, 0, s), b))),
        App(f, a) => App(Box::new(subst(j, s, f)), Box::new(subst(j, s, a))),
    }
}

/// (\x. body) arg  ->  body[x := arg], the lambda removed.
pub fn beta(body: &Term, arg: &Term) -> Term {
    shift(-1, 0, &subst(0, &shift(1, 0, arg), body))
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Strategy {
    Normal,      // leftmost outermost redex, also under lambda
    ByName,      // leftmost outermost, never under lambda, never in an argument
    ByValue,     // arguments reduced to values first, never under lambda
    Applicative, // leftmost innermost, also under lambda
}

fn is_value(t: &Term) -> bool {
    !matches!(t, App(..))
}

/// One step of the strategy, or None if it finds no redex.
pub fn step(t: &Term, s: Strategy) -> Option<Term> {
    use Strategy::*;
    match t {
        Var(_) | Free(_) => None,
        Lam(x, b) => match s {
            Normal | Applicative => step(b, s).map(|b| Lam(x.clone(), Box::new(b))),
            ByName | ByValue => None,
        },
        App(f, a) => {
            let redex = |f: &Term| if let Lam(_, b) = f { Some(beta(b, a)) } else { None };
            match s {
                Normal | ByName => redex(f).or_else(|| match step(f, s) {
                    Some(f2) => Some(App(Box::new(f2), a.clone())),
                    None if s == Normal => step(a, s).map(|a2| App(f.clone(), Box::new(a2))),
                    None => None,
                }),
                ByValue | Applicative => {
                    if s == Applicative || !is_value(f) {
                        if let Some(f2) = step(f, s) {
                            return Some(App(Box::new(f2), a.clone()));
                        }
                    }
                    if s == Applicative || !is_value(a) {
                        if let Some(a2) = step(a, s) {
                            return Some(App(f.clone(), Box::new(a2)));
                        }
                    }
                    redex(f)
                }
            }
        }
    }
}

/// Reduce until no redex is left or `limit` steps are made.
pub fn run(t: &Term, s: Strategy, limit: usize) -> (Term, usize, bool) {
    let mut t = t.clone();
    for n in 0..limit {
        match step(&t, s) {
            Some(t2) => t = t2,
            None => return (t, n, true),
        }
    }
    (t, limit, false)
}
