// smallstep.rs -- call-by-value small-step semantics of the lambda-language:
// one case per rule, substitution of closed values.
#![allow(dead_code)]
use crate::lam::{b, show, Op, E};

pub fn is_value(e: &E) -> bool {
    match e {
        E::Int(_) | E::Bool(_) | E::Lam(..) => true,
        E::Pair(a, c) => is_value(a) && is_value(c),
        _ => false,
    }
}

/// e[x := v] for a closed value v: nothing in v can be captured.
pub fn subst(e: &E, x: &str, v: &E) -> E {
    let s = |e: &E| b(subst(e, x, v));
    match e {
        E::Var(y) if y == x => v.clone(),
        E::Lam(y, t, body) if y != x => E::Lam(y.clone(), t.clone(), s(body)),
        E::App(f, a) => E::App(s(f), s(a)),
        E::Let(y, a, body) => E::Let(y.clone(), s(a), if y == x { body.clone() } else { s(body) }),
        E::LetRec(y, a, body) if y != x => E::LetRec(y.clone(), s(a), s(body)),
        E::Op(op, a, c) => E::Op(*op, s(a), s(c)),
        E::If(c, t, f) => E::If(s(c), s(t), s(f)),
        E::Pair(a, c) => E::Pair(s(a), s(c)),
        E::Fst(a) => E::Fst(s(a)),
        E::Snd(a) => E::Snd(s(a)),
        _ => e.clone(), // a constant, another variable, or a binder of x
    }
}

/// letrec f = \x. e1 unfolds to \x. letrec f = \x. e1 in e1.
pub fn unfold(f: &str, lam: &E) -> E {
    match lam {
        E::Lam(x, t, e1) => {
            E::Lam(x.clone(), t.clone(), b(E::LetRec(f.to_string(), b(lam.clone()), e1.clone())))
        }
        _ => unreachable!("the parser only accepts letrec of a lambda"),
    }
}

pub fn arith(op: Op, a: &E, c: &E) -> Result<E, String> {
    Ok(match (op, a, c) {
        (Op::Add, E::Int(x), E::Int(y)) => E::Int(x.wrapping_add(*y)),
        (Op::Sub, E::Int(x), E::Int(y)) => E::Int(x.wrapping_sub(*y)),
        (Op::Mul, E::Int(x), E::Int(y)) => E::Int(x.wrapping_mul(*y)),
        (Op::Lt, E::Int(x), E::Int(y)) => E::Bool(x < y),
        (Op::Eq, E::Int(x), E::Int(y)) => E::Bool(x == y),
        (Op::Eq, E::Bool(x), E::Bool(y)) => E::Bool(x == y),
        _ => return Err(format!("'{}' cannot apply to {} and {}", op.symbol(), show(a), show(c))),
    })
}

/// One step of a term that is not a value; Err if it is stuck.
pub fn step(e: &E) -> Result<E, String> {
    let st = |e: &E| step(e).map(b);
    Ok(match e {
        E::App(f, a) if !is_value(f) => E::App(st(f)?, a.clone()),
        E::App(f, a) if !is_value(a) => E::App(f.clone(), st(a)?),
        E::App(f, v) => match &**f {
            E::Lam(x, _, body) => subst(body, x, v), // beta for values
            _ => return Err(format!("{} is not a function", show(f))),
        },
        E::Let(x, a, body) if !is_value(a) => E::Let(x.clone(), st(a)?, body.clone()),
        E::Let(x, v, body) => subst(body, x, v),
        E::LetRec(f, lam, body) => subst(body, f, &unfold(f, lam)),
        E::Op(op, a, c) if !is_value(a) => E::Op(*op, st(a)?, c.clone()),
        E::Op(op, a, c) if !is_value(c) => E::Op(*op, a.clone(), st(c)?),
        E::Op(op, a, c) => arith(*op, a, c)?,
        E::If(c, t, f) if !is_value(c) => E::If(st(c)?, t.clone(), f.clone()),
        E::If(c, t, f) => match **c {
            E::Bool(true) => (**t).clone(),
            E::Bool(false) => (**f).clone(),
            _ => return Err(format!("the condition {} is not a boolean", show(c))),
        },
        E::Pair(a, c) if !is_value(a) => E::Pair(st(a)?, c.clone()),
        E::Pair(a, c) => E::Pair(a.clone(), st(c)?),
        E::Fst(p) | E::Snd(p) if !is_value(p) => {
            let p2 = st(p)?;
            if matches!(e, E::Fst(_)) { E::Fst(p2) } else { E::Snd(p2) }
        }
        E::Fst(p) | E::Snd(p) => match &**p {
            E::Pair(a, c) => if matches!(e, E::Fst(_)) { (**a).clone() } else { (**c).clone() },
            _ => return Err(format!("{} is not a pair", show(p))),
        },
        E::Var(x) => return Err(format!("'{x}' is not bound")),
        E::Int(_) | E::Bool(_) | E::Lam(..) => return Err("a value makes no step".into()),
    })
}

/// Step until a value, an error, or `fuel` steps; `see` gets every term.
pub fn run(e: &E, fuel: usize, see: &mut dyn FnMut(usize, &E)) -> (Result<E, String>, usize) {
    let mut e = e.clone();
    for n in 0..fuel {
        see(n, &e);
        if is_value(&e) {
            return (Ok(e), n);
        }
        match step(&e) {
            Ok(e2) => e = e2,
            Err(msg) => return (Err(msg), n),
        }
    }
    (Err(format!("no value after {fuel} steps")), fuel)
}
