// check.rs -- the simply typed lambda-language: every parameter carries
// its type, and the checker builds the derivation of e : t.
#![allow(dead_code)]
use crate::lam::{show, show_ty, Op, Ty, E};

pub type Ctx = Vec<(String, Ty)>; // the last binding of a name wins

/// One node: the rule used, its conclusion ctx |- e : ty, its premises.
pub struct Deriv {
    pub rule: &'static str,
    pub ctx: Ctx,
    pub e: E,
    pub ty: Ty,
    pub premises: Vec<Deriv>,
}

pub fn derive(ctx: &Ctx, e: &E) -> Result<Deriv, String> {
    let node = |rule, ty, premises| {
        Ok(Deriv { rule, ctx: ctx.clone(), e: e.clone(), ty, premises })
    };
    match e {
        E::Int(_) => node("int", Ty::Int, vec![]),
        E::Bool(_) => node("bool", Ty::Bool, vec![]),
        E::Var(x) => match ctx.iter().rev().find(|(y, _)| y == x) {
            Some((_, t)) => node("var", t.clone(), vec![]),
            None => Err(format!("'{x}' is not in the context")),
        },
        E::Lam(x, Some(a), body) => {
            let mut c2 = ctx.clone();
            c2.push((x.clone(), a.clone()));
            let d = derive(&c2, body)?;
            let t = Ty::Fun(Box::new(a.clone()), Box::new(d.ty.clone()));
            node("abs", t, vec![d])
        }
        E::Lam(x, None, _) => Err(format!("the parameter '{x}' has no type")),
        E::App(f, a) => {
            let (df, da) = (derive(ctx, f)?, derive(ctx, a)?);
            match &df.ty {
                Ty::Fun(p, r) if **p == da.ty => {
                    let r = (**r).clone();
                    node("app", r, vec![df, da])
                }
                Ty::Fun(p, _) => {
                    Err(format!("{} expects {}, not {}", show(f), show_ty(p), show_ty(&da.ty)))
                }
                t => Err(format!("{} has type {}, not a function", show(f), show_ty(t))),
            }
        }
        E::Let(x, e1, e2) => {
            let d1 = derive(ctx, e1)?;
            let mut c2 = ctx.clone();
            c2.push((x.clone(), d1.ty.clone()));
            let d2 = derive(&c2, e2)?;
            let t = d2.ty.clone();
            node("let", t, vec![d1, d2])
        }
        E::Op(op, a, b) => {
            let (da, db) = (derive(ctx, a)?, derive(ctx, b)?);
            if da.ty != Ty::Int || db.ty != Ty::Int {
                return Err(format!("'{}' needs two ints", op.symbol()));
            }
            let t = if matches!(op, Op::Eq | Op::Lt) { Ty::Bool } else { Ty::Int };
            node("op", t, vec![da, db])
        }
        E::If(c, t, f) => {
            let (dc, dt, df) = (derive(ctx, c)?, derive(ctx, t)?, derive(ctx, f)?);
            if dc.ty != Ty::Bool {
                return Err(format!("the condition {} is not a bool", show(c)));
            }
            if dt.ty != df.ty {
                let (a, b) = (show_ty(&dt.ty), show_ty(&df.ty));
                return Err(format!("the branches have types {a} and {b}"));
            }
            let ty = dt.ty.clone();
            node("if", ty, vec![dc, dt, df])
        }
        E::LetRec(..) => Err("letrec needs the result type too: see inference".into()),
        E::Pair(..) | E::Fst(_) | E::Snd(_) => Err("no pairs in the core: exercise 6".into()),
    }
}

/// Print the derivation, conclusion first, premises indented below.
pub fn print(d: &Deriv, depth: usize, out: &mut Vec<String>) {
    let ctx: Vec<String> = d.ctx.iter().map(|(x, t)| format!("{x}: {}", show_ty(t))).collect();
    let gamma = if ctx.is_empty() { String::new() } else { ctx.join(", ") + " " };
    let (e, t) = (show(&d.e), show_ty(&d.ty));
    out.push(format!("{}{gamma}|- {e} : {t}   [{}]", "  ".repeat(depth), d.rule));
    for p in &d.premises {
        print(p, depth + 1, out);
    }
}
