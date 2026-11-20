// infer.rs -- type inference for the lambda-language: fresh variables,
// unification, and generalisation at let (algorithm W).
#![allow(dead_code)]
use crate::lam::{Op, Ty, E};
use crate::unify::{apply, type_vars, unify, Subst};
use std::collections::BTreeSet;

/// forall vars. ty
#[derive(Clone, Debug)]
pub struct Scheme {
    pub vars: Vec<u32>,
    pub ty: Ty,
}

pub fn mono(t: Ty) -> Scheme {
    Scheme { vars: vec![], ty: t }
}

pub struct Infer<'a> {
    pub s: Subst,
    next: u32,
    pub generalise: bool,
    pub on_let: &'a mut dyn FnMut(&str, &Scheme),
}

pub type Env = Vec<(String, Scheme)>;

impl<'a> Infer<'a> {
    pub fn new(on_let: &'a mut dyn FnMut(&str, &Scheme)) -> Self {
        Infer { s: Subst::new(), next: 0, generalise: true, on_let }
    }
    fn fresh(&mut self) -> Ty {
        self.next += 1;
        Ty::Var(self.next - 1)
    }
    /// A fresh copy of the scheme's type, its bound variables renamed.
    fn instantiate(&mut self, sc: &Scheme) -> Ty {
        let fresh: Subst = sc.vars.iter().map(|&v| (v, self.fresh())).collect();
        apply(&fresh, &sc.ty)
    }
    /// Quantify the variables of t that are not free in the environment.
    fn gen(&self, env: &Env, t: &Ty) -> Scheme {
        let t = apply(&self.s, t);
        if !self.generalise {
            return mono(t);
        }
        let mut in_env = BTreeSet::new();
        for (_, sc) in env {
            let mut vs = BTreeSet::new();
            type_vars(&apply(&self.s, &sc.ty), &mut vs);
            in_env.extend(vs.into_iter().filter(|v| !sc.vars.contains(v)));
        }
        let mut vs = BTreeSet::new();
        type_vars(&t, &mut vs);
        Scheme { vars: vs.difference(&in_env).copied().collect(), ty: t }
    }

    pub fn infer(&mut self, env: &Env, e: &E) -> Result<Ty, String> {
        let t = match e {
            E::Int(_) => Ty::Int,
            E::Bool(_) => Ty::Bool,
            E::Var(x) => match env.iter().rev().find(|(y, _)| y == x) {
                Some((_, sc)) => self.instantiate(&sc.clone()),
                None => return Err(format!("'{x}' is not bound")),
            },
            E::Lam(x, ann, body) => {
                let a = ann.clone().unwrap_or_else(|| self.fresh());
                let mut env2 = env.clone();
                env2.push((x.clone(), mono(a.clone())));
                let r = self.infer(&env2, body)?;
                Ty::Fun(Box::new(a), Box::new(r))
            }
            E::App(f, arg) => {
                let tf = self.infer(env, f)?;
                let ta = self.infer(env, arg)?;
                let r = self.fresh();
                self.unify(&tf, &Ty::Fun(Box::new(ta), Box::new(r.clone())))?;
                r
            }
            E::Let(x, e1, e2) | E::LetRec(x, e1, e2) => {
                let mut env1 = env.clone();
                let rec = matches!(e, E::LetRec(..)).then(|| self.fresh());
                if let Some(a) = &rec {
                    env1.push((x.clone(), mono(a.clone()))); // f is monomorphic in its body
                }
                let t1 = self.infer(&env1, e1)?;
                if let Some(a) = &rec {
                    self.unify(a, &t1)?;
                }
                let sc = self.gen(env, &t1);
                (self.on_let)(x, &sc);
                let mut env2 = env.clone();
                env2.push((x.clone(), sc));
                self.infer(&env2, e2)?
            }
            E::Op(op, a, b) => {
                let (ta, tb) = (self.infer(env, a)?, self.infer(env, b)?);
                self.unify(&ta, &Ty::Int)?;
                self.unify(&tb, &Ty::Int)?;
                if matches!(op, Op::Eq | Op::Lt) { Ty::Bool } else { Ty::Int }
            }
            E::If(c, t, f) => {
                let tc = self.infer(env, c)?;
                self.unify(&tc, &Ty::Bool)?;
                let (tt, tf) = (self.infer(env, t)?, self.infer(env, f)?);
                self.unify(&tt, &tf)?;
                tt
            }
            E::Pair(a, b) => {
                let (ta, tb) = (self.infer(env, a)?, self.infer(env, b)?);
                Ty::Pair(Box::new(ta), Box::new(tb))
            }
            E::Fst(p) | E::Snd(p) => {
                let tp = self.infer(env, p)?;
                let (a, b) = (self.fresh(), self.fresh());
                self.unify(&tp, &Ty::Pair(Box::new(a.clone()), Box::new(b.clone())))?;
                if matches!(e, E::Fst(_)) { a } else { b }
            }
        };
        Ok(apply(&self.s, &t))
    }

    fn unify(&mut self, a: &Ty, b: &Ty) -> Result<(), String> {
        unify(&mut self.s, a, b).map_err(|m| format!("type error: {m}"))
    }
}

/// The principal type of a closed expression, its variables renamed.
pub fn principal(e: &E) -> Result<Ty, String> {
    let mut quiet = |_: &str, _: &Scheme| {};
    let mut inf = Infer::new(&mut quiet);
    inf.infer(&vec![], e).map(|t| crate::unify::normalise(&t))
}
