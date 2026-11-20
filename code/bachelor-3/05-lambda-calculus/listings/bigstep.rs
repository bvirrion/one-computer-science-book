// bigstep.rs -- the big-step rules of the lambda-language read as an evaluator:
// each call is one node of the derivation e => v.
#![allow(dead_code)]
use crate::lam::{b, show, E};
use crate::smallstep::{arith, subst, unfold};

#[derive(Default, Debug)]
pub struct Size {
    pub nodes: usize,        // rule applications in the derivation
    pub contractions: usize, // nodes whose rule computes (beta, let, op, if, ...)
    pub depth: usize,
}

pub fn eval(e: &E, z: &mut Size, depth: usize) -> Result<E, String> {
    z.nodes += 1;
    z.depth = z.depth.max(depth + 1);
    let ev = |e: &E, z: &mut Size| eval(e, z, depth + 1);
    if !matches!(e, E::Int(_) | E::Bool(_) | E::Lam(..) | E::Pair(..) | E::Var(_)) {
        z.contractions += 1;
    }
    match e {
        E::Int(_) | E::Bool(_) | E::Lam(..) => Ok(e.clone()), // a value evaluates to itself
        E::Var(x) => Err(format!("'{x}' is not bound")),
        E::App(f, a) => {
            let f = ev(f, z)?;
            let v = ev(a, z)?;
            match f {
                E::Lam(x, _, body) => ev(&subst(&body, &x, &v), z),
                _ => Err(format!("{} is not a function", show(&f))),
            }
        }
        E::Let(x, a, body) => {
            let v = ev(a, z)?;
            ev(&subst(body, x, &v), z)
        }
        E::LetRec(f, lam, body) => ev(&subst(body, f, &unfold(f, lam)), z),
        E::Op(op, a, c) => {
            let va = ev(a, z)?;
            let vc = ev(c, z)?;
            arith(*op, &va, &vc)
        }
        E::If(c, t, f) => match ev(c, z)? {
            E::Bool(true) => ev(t, z),
            E::Bool(false) => ev(f, z),
            other => Err(format!("the condition {} is not a boolean", show(&other))),
        },
        E::Pair(a, c) => Ok(E::Pair(b(ev(a, z)?), b(ev(c, z)?))),
        E::Fst(p) | E::Snd(p) => match ev(p, z)? {
            E::Pair(a, c) => Ok(if matches!(e, E::Fst(_)) { *a } else { *c }),
            other => Err(format!("{} is not a pair", show(&other))),
        },
    }
}
