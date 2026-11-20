// ex12_krivine.rs -- exercise 12: the Krivine machine. A closure is a term
// with its environment; the machine needs no substitution.
#![allow(dead_code)]
use crate::reduce::shift;
use crate::term::{Term, Term::*};
use std::rc::Rc;

#[derive(Clone)]
pub struct Closure {
    pub term: Term,
    pub env: Rc<Vec<Closure>>, // index 0 is the innermost binder
}

/// Run to weak head normal form; returns the read-back term and the number
/// of β-steps (pops), or None if `limit` transitions are not enough.
pub fn krivine(t: &Term, limit: usize) -> Option<(Term, usize)> {
    let mut c = Closure { term: t.clone(), env: Rc::new(vec![]) };
    let mut stack: Vec<Closure> = vec![];
    let mut betas = 0;
    for _ in 0..limit {
        match c.term.clone() {
            App(f, a) => {
                stack.push(Closure { term: *a, env: c.env.clone() });
                c.term = *f;
            }
            Lam(_, b) if !stack.is_empty() => {
                let arg = stack.pop().unwrap();
                let mut env = (*c.env).clone();
                env.insert(0, arg);
                c = Closure { term: *b, env: Rc::new(env) };
                betas += 1;
            }
            Var(k) => c = c.env[k].clone(),
            Lam(..) | Free(_) => {
                let mut out = readback(&c);
                while let Some(arg) = stack.pop() {
                    out = App(Box::new(out), Box::new(readback(&arg)));
                }
                return Some((out, betas));
            }
        }
    }
    None
}

/// The term a closure stands for: its free indices replaced by the
/// environment's closures, read back in turn.
pub fn readback(c: &Closure) -> Term {
    fn go(t: &Term, env: &[Closure], depth: usize) -> Term {
        match t {
            Var(k) if *k < depth => Var(*k),
            Var(k) => shift(depth as isize, 0, &readback(&env[*k - depth])),
            Free(x) => Free(x.clone()),
            Lam(x, b) => Lam(x.clone(), Box::new(go(b, env, depth + 1))),
            App(f, a) => App(Box::new(go(f, env, depth)), Box::new(go(a, env, depth))),
        }
    }
    go(&c.term, &c.env, 0)
}
