// ex6_pairs.rs -- exercise 6: the checker's typing function, with pairs.
#![allow(dead_code)]
use crate::lam::{show_ty, Op, Ty, E};

pub fn type_of(ctx: &[(String, Ty)], e: &E) -> Result<Ty, String> {
    let ty = |e: &E| type_of(ctx, e);
    Ok(match e {
        E::Int(_) => Ty::Int,
        E::Bool(_) => Ty::Bool,
        E::Var(x) => ctx.iter().rev().find(|(y, _)| y == x).map(|(_, t)| t.clone())
            .ok_or(format!("'{x}' is not in the context"))?,
        E::Lam(x, Some(a), body) => {
            let mut c2 = ctx.to_vec();
            c2.push((x.clone(), a.clone()));
            Ty::Fun(Box::new(a.clone()), Box::new(type_of(&c2, body)?))
        }
        E::App(f, a) => match (ty(f)?, ty(a)?) {
            (Ty::Fun(p, r), ta) if *p == ta => *r,
            (tf, ta) => return Err(format!("cannot apply {} to {}", show_ty(&tf), show_ty(&ta))),
        },
        E::Let(x, e1, e2) => {
            let mut c2 = ctx.to_vec();
            c2.push((x.clone(), ty(e1)?));
            type_of(&c2, e2)?
        }
        E::Op(op, a, b) => match (ty(a)?, ty(b)?) {
            (Ty::Int, Ty::Int) if matches!(op, Op::Eq | Op::Lt) => Ty::Bool,
            (Ty::Int, Ty::Int) => Ty::Int,
            _ => return Err(format!("'{}' needs two ints", op.symbol())),
        },
        E::If(c, t, f) => match (ty(c)?, ty(t)?, ty(f)?) {
            (Ty::Bool, a, b) if a == b => a,
            _ => return Err("bad if".into()),
        },
        // the three new rules
        E::Pair(a, b) => Ty::Pair(Box::new(ty(a)?), Box::new(ty(b)?)),
        E::Fst(p) | E::Snd(p) => match ty(p)? {
            Ty::Pair(a, b) => if matches!(e, E::Fst(_)) { *a } else { *b },
            t => return Err(format!("{} is not a pair type", show_ty(&t))),
        },
        E::Lam(x, None, _) => return Err(format!("the parameter '{x}' has no type")),
        E::LetRec(..) => return Err("letrec needs the result type".into()),
    })
}
