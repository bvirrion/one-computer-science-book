// typecheck.rs -- the static semantics of Moor: the type of every
// expression, checked against the typing rules. Frozen for the book.
#![allow(dead_code)]
use crate::ast::*;
use crate::resolve::{self, Diag, Kind, Resolution, NOWHERE};
use crate::token::Span;
use std::collections::HashMap;

/// `Error` is the type of an expression already reported as wrong: it is
/// accepted everywhere, so one mistake gives one message.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Ty { Int, Bool, Unit, Error }

impl Ty {
    pub fn of(t: Type) -> Ty {
        match t { Type::Int => Ty::Int, Type::Bool => Ty::Bool }
    }
    pub fn name(self) -> &'static str {
        match self { Ty::Int => "int", Ty::Bool => "bool", Ty::Unit => "nothing", Ty::Error => "error" }
    }
}

pub struct Checker<'a> {
    r: &'a Resolution,
    pub decl_ty: HashMap<usize, Ty>,             // variables and parameters
    sigs: HashMap<usize, (Vec<Ty>, Ty, String)>, // functions: params, result, name
    ret: Ty,                                     // the current function's result
    pub errors: Vec<Diag>,
}

pub fn check<'a>(p: &Program, r: &'a Resolution) -> Checker<'a> {
    let mut c = Checker { r, decl_ty: HashMap::new(), sigs: HashMap::new(), ret: Ty::Unit, errors: vec![] };
    c.sigs.insert(0, (vec![Ty::Int], Ty::Unit, "print".into()));
    c.sigs.insert(1, (vec![Ty::Int], Ty::Unit, "print_char".into()));
    c.sigs.insert(2, (vec![], Ty::Int, "read".into()));
    for (item, &id) in p.items.iter().zip(&r.items) {
        match item {
            Item::Func(f) => {
                let ps = f.params.iter().map(|q| Ty::of(q.ty)).collect();
                c.sigs.insert(id, (ps, f.ret.map_or(Ty::Unit, Ty::of), f.name.clone()));
            }
            Item::Global { ty, init, span, .. } => {
                c.decl_ty.insert(id, Ty::of(*ty));
                if let Some(e) = init {
                    let t = c.expr(e);
                    c.expect(t, Ty::of(*ty), *span, "the initial value of a global");
                }
            }
            Item::Array { .. } => {}
        }
    }
    let main = p.items.iter().find_map(|i| match i { Item::Func(f) if f.name == "main" => Some(f), _ => None });
    match main {
        None => c.error("the program has no main function".into(), NOWHERE),
        Some(f) if !f.params.is_empty() => c.error("main takes no parameters".into(), f.span),
        Some(f) if f.ret == Some(Type::Bool) => c.error("main returns an int or nothing".into(), f.span),
        _ => {}
    }
    for item in &p.items {
        if let Item::Func(f) = item {
            c.func(f);
        }
    }
    c
}

impl Checker<'_> {
    fn error(&mut self, msg: String, span: Span) {
        self.errors.push(Diag { msg, span, note: None });
    }
    /// Report unless `got` is the expected type or already an error.
    fn expect(&mut self, got: Ty, want: Ty, span: Span, what: &str) {
        if got != want && got != Ty::Error {
            self.error(format!("{what} must be {}, found {}", article(want), article(got)), span);
        }
    }

    fn func(&mut self, f: &Func) {
        for q in &f.params {
            self.decl_ty.insert(self.r.defs[&q.span.start], Ty::of(q.ty));
        }
        self.ret = f.ret.map_or(Ty::Unit, Ty::of);
        self.block(&f.body);
        if self.ret != Ty::Unit && !returns(&f.body) {
            self.error(format!("'{}' can reach its end without returning {}", f.name, article(self.ret)), f.span);
        }
    }

    fn block(&mut self, b: &Block) {
        for s in &b.stmts {
            self.stmt(s);
        }
    }

    fn stmt(&mut self, s: &Stmt) {
        match &s.kind {
            StmtKind::Var(x, ann, e) => {
                let t = self.expr(e);
                let t = match (ann, t) {
                    (_, Ty::Unit) => {
                        self.error(format!("'{x}' is initialised with a call that returns nothing"), e.span);
                        Ty::Error
                    }
                    (Some(a), _) => {
                        self.expect(t, Ty::of(*a), e.span, &format!("the initial value of '{x}'"));
                        Ty::of(*a)
                    }
                    (None, t) => t,
                };
                self.decl_ty.insert(self.r.defs[&s.span.start], t);
            }
            StmtKind::Assign(x, e) => {
                let target = self.var_type(x, s.span);
                let t = self.expr(e);
                if target != Ty::Error {
                    self.expect(t, target, e.span, &format!("the value assigned to '{x}'"));
                }
            }
            StmtKind::AssignIndex(a, i, e) => {
                self.array(a, s.span);
                let ti = self.expr(i);
                self.expect(ti, Ty::Int, i.span, "an array index");
                let te = self.expr(e);
                self.expect(te, Ty::Int, e.span, "an array element");
            }
            StmtKind::If(c, t, f) => {
                let tc = self.expr(c);
                self.expect(tc, Ty::Bool, c.span, "the condition of an if");
                self.block(t);
                if let Some(f) = f {
                    self.block(f);
                }
            }
            StmtKind::While(c, b) => {
                let tc = self.expr(c);
                self.expect(tc, Ty::Bool, c.span, "the condition of a while");
                self.block(b);
            }
            StmtKind::Return(e) => match (e, self.ret) {
                (None, Ty::Unit) => {}
                (None, r) => self.error(format!("this function must return {}", article(r)), s.span),
                (Some(e), Ty::Unit) => {
                    self.expr(e);
                    self.error("this function returns nothing, but the return has a value".into(), e.span);
                }
                (Some(e), r) => {
                    let t = self.expr(e);
                    self.expect(t, r, e.span, "the returned value");
                }
            },
            StmtKind::Expr(e) => {
                self.expr(e);
            }
            StmtKind::Block(b) => self.block(b),
        }
    }

    /// The type of a variable named in an assignment or an expression.
    fn var_type(&mut self, x: &str, span: Span) -> Ty {
        let Some(&id) = self.r.uses.get(&span.start) else { return Ty::Error };
        match self.r.decls[id].kind {
            Kind::Local | Kind::Param | Kind::Global => self.decl_ty.get(&id).copied().unwrap_or(Ty::Error),
            Kind::Array => self.misuse(x, "an array", span),
            Kind::Func | Kind::Builtin => self.misuse(x, "a function", span),
        }
    }
    fn misuse(&mut self, x: &str, what: &str, span: Span) -> Ty {
        self.error(format!("'{x}' is {what}, not a variable"), span);
        Ty::Error
    }
    fn array(&mut self, a: &str, span: Span) -> bool {
        let Some(&id) = self.r.uses.get(&span.start) else { return false };
        if self.r.decls[id].kind != Kind::Array {
            self.error(format!("'{a}' is not an array"), span);
            return false;
        }
        true
    }

    pub fn expr(&mut self, e: &Expr) -> Ty {
        match &e.kind {
            ExprKind::Int(_) => Ty::Int,
            ExprKind::Bool(_) => Ty::Bool,
            ExprKind::Var(x) => self.var_type(x, e.span),
            ExprKind::Unary(op, a) => {
                let (want, sym) = if *op == UnOp::Neg { (Ty::Int, "-") } else { (Ty::Bool, "!") };
                let t = self.expr(a);
                self.expect(t, want, a.span, &format!("the operand of '{sym}'"));
                want
            }
            ExprKind::Binary(op, a, b) => self.binary(*op, a, b),
            ExprKind::Call(f, args) => self.call(f, args, e.span),
            ExprKind::Index(a, i) => {
                let ok = self.array(a, e.span);
                let t = self.expr(i);
                self.expect(t, Ty::Int, i.span, "an array index");
                if ok { Ty::Int } else { Ty::Error }
            }
        }
    }

    fn binary(&mut self, op: BinOp, a: &Expr, b: &Expr) -> Ty {
        use BinOp::*;
        let (ta, tb) = (self.expr(a), self.expr(b));
        let sym = op.symbol();
        let (operand, result) = match op {
            Add | Sub | Mul | Div | Rem => (Ty::Int, Ty::Int),
            Lt | Le | Gt | Ge => (Ty::Int, Ty::Bool),
            And | Or => (Ty::Bool, Ty::Bool),
            Eq | Ne => {
                if ta == Ty::Unit || tb == Ty::Unit {
                    let at = if ta == Ty::Unit { a.span } else { b.span };
                    self.error(format!("'{sym}' cannot compare nothing"), at);
                } else if ta != tb && ta != Ty::Error && tb != Ty::Error {
                    let (x, y) = (article(ta), article(tb));
                    self.error(format!("'{sym}' compares {x} with {y}"), b.span);
                }
                return Ty::Bool;
            }
        };
        self.expect(ta, operand, a.span, &format!("the left operand of '{sym}'"));
        self.expect(tb, operand, b.span, &format!("the right operand of '{sym}'"));
        result
    }

    fn call(&mut self, f: &str, args: &[Expr], span: Span) -> Ty {
        let arg_tys: Vec<Ty> = args.iter().map(|a| self.expr(a)).collect();
        let Some(&id) = self.r.uses.get(&span.start) else { return Ty::Error };
        let Some((params, ret, _)) = self.sigs.get(&id).cloned() else {
            self.error(format!("'{f}' is not a function"), span);
            return Ty::Error;
        };
        if params.len() != args.len() {
            let n = params.len();
            self.error(format!("'{f}' takes {n} argument{}, but {} {} given", if n == 1 { "" } else { "s" },
                               args.len(), if args.len() == 1 { "is" } else { "are" }), span);
            return ret;
        }
        for (k, (a, (&t, &p))) in args.iter().zip(arg_tys.iter().zip(&params)).enumerate() {
            self.expect(t, p, a.span, &format!("argument {} of '{f}'", k + 1));
        }
        ret
    }
}

fn article(t: Ty) -> String {
    match t {
        Ty::Int => "an int".into(),
        Ty::Bool => "a bool".into(),
        t => t.name().into(),
    }
}

/// Does every path through the block end in a return?
pub fn returns(b: &Block) -> bool {
    b.stmts.iter().any(|s| match &s.kind {
        StmtKind::Return(_) => true,
        StmtKind::If(_, t, Some(f)) => returns(t) && returns(f),
        StmtKind::Block(b) => returns(b),
        _ => false,
    })
}

/// The whole front end: lex, parse, resolve, check. Every error is shown,
/// in the order of the source.
pub fn check_source(src: &str, file: &str) -> Result<(Program, Resolution, HashMap<usize, Ty>), String> {
    let prog = crate::parser::parse_source(src, file)?;
    let r = resolve::resolve(&prog);
    let c = check(&prog, &r);
    let mut errs: Vec<Diag> = r.errors.iter().chain(&c.errors).cloned().collect();
    if errs.is_empty() {
        let tys = c.decl_ty;
        return Ok((prog, r, tys));
    }
    errs.sort_by_key(|d| d.span.start);
    Err(errs.iter().map(|d| resolve::render(src, file, d)).collect())
}
