// tac.rs -- three-address code for Moor: at most one operator per
// instruction, control flow as labels and jumps, every value in a temporary.
#![allow(dead_code)]
use crate::ast::*;
use crate::resolve::{Kind, Resolution};
use std::collections::HashMap;

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum Val {
    T(u32),  // a temporary: a local, a parameter or an intermediate result
    K(i32),  // a constant
}

#[derive(Clone, Debug, PartialEq)]
pub enum Tac {
    Bin(u32, BinOp, Val, Val),         // t = a op b, op neither && nor ||
    Neg(u32, Val),                     // t = -a
    Not(u32, Val),                     // t = !a
    Copy(u32, Val),                    // t = a
    LoadG(u32, String),                // t = g
    StoreG(String, Val),               // g = a
    LoadA(u32, String, Val),           // t = arr[i]
    StoreA(String, Val, Val),          // arr[i] = a
    Label(u32),                        // L:
    Jump(u32),                         // goto L
    Branch(BinOp, Val, Val, u32),      // if a rel b goto L
    Call(Option<u32>, String, Vec<Val>),
    Ret(Option<Val>),
}

pub struct FuncTac {
    pub name: String,
    pub params: Vec<u32>,
    pub code: Vec<Tac>,
    pub temps: u32,
    pub names: HashMap<u32, String>, // temporaries that hold a variable
}

struct Gen<'a> {
    r: &'a Resolution,
    var_temp: HashMap<usize, u32>, // declaration -> its temporary
    f: FuncTac,
    labels: u32,
}

pub fn translate(p: &Program, r: &Resolution) -> Vec<FuncTac> {
    let mut out = vec![];
    for item in &p.items {
        if let Item::Func(func) = item {
            let f = FuncTac { name: func.name.clone(), params: vec![], code: vec![], temps: 0,
                              names: HashMap::new() };
            let mut g = Gen { r, var_temp: HashMap::new(), f, labels: 0 };
            for prm in &func.params {
                let t = g.declare(prm.span.start, &prm.name);
                g.f.params.push(t);
            }
            g.block(&func.body);
            g.emit(Tac::Ret(None)); // reached only by a function without a result
            out.push(g.f);
        }
    }
    out
}

impl Gen<'_> {
    fn emit(&mut self, t: Tac) {
        self.f.code.push(t);
    }
    fn temp(&mut self) -> u32 {
        self.f.temps += 1;
        self.f.temps - 1
    }
    fn label(&mut self) -> u32 {
        self.labels += 1;
        self.labels
    }
    fn declare(&mut self, def: usize, name: &str) -> u32 {
        let t = self.temp();
        self.var_temp.insert(self.r.defs[&def], t);
        let taken = self.f.names.values().any(|n| n == name);
        self.f.names.insert(t, if taken { format!("{name}.{t}") } else { name.to_string() });
        t
    }
    /// The declaration a use refers to, as its temporary or its global name.
    fn place(&self, use_at: usize) -> Result<u32, String> {
        let d = self.r.uses[&use_at];
        match self.r.decls[d].kind {
            Kind::Local | Kind::Param => Ok(self.var_temp[&d]),
            _ => Err(self.r.decls[d].name.clone()),
        }
    }

    fn expr(&mut self, e: &Expr) -> Val {
        match &e.kind {
            ExprKind::Int(n) => Val::K(*n as i32),
            ExprKind::Bool(b) => Val::K(*b as i32),
            ExprKind::Var(_) => match self.place(e.span.start) {
                Ok(t) => Val::T(t),
                Err(g) => { let t = self.temp(); self.emit(Tac::LoadG(t, g)); Val::T(t) }
            },
            ExprKind::Unary(UnOp::Neg, a) if matches!(a.kind, ExprKind::Int(_)) => {
                let ExprKind::Int(n) = a.kind else { unreachable!() };
                Val::K((n as i32).wrapping_neg()) // a negative literal
            }
            ExprKind::Unary(op, a) => {
                let v = self.expr(a);
                let t = self.temp();
                self.emit(if *op == UnOp::Neg { Tac::Neg(t, v) } else { Tac::Not(t, v) });
                Val::T(t)
            }
            ExprKind::Binary(BinOp::And | BinOp::Or, ..) => {
                // a value from jumping code: t = 1 on one path, 0 on the other
                let (t, yes, no, end) = (self.temp(), self.label(), self.label(), self.label());
                self.cond(e, yes, no);
                self.emit(Tac::Label(yes));
                self.emit(Tac::Copy(t, Val::K(1)));
                self.emit(Tac::Jump(end));
                self.emit(Tac::Label(no));
                self.emit(Tac::Copy(t, Val::K(0)));
                self.emit(Tac::Label(end));
                Val::T(t)
            }
            ExprKind::Binary(op, a, b) => {
                let (va, vb) = (self.expr(a), self.expr(b));
                let t = self.temp();
                self.emit(Tac::Bin(t, *op, va, vb));
                Val::T(t)
            }
            ExprKind::Call(f, args) => {
                let vs = args.iter().map(|a| self.expr(a)).collect();
                let t = self.temp();
                self.emit(Tac::Call(Some(t), f.clone(), vs));
                Val::T(t)
            }
            ExprKind::Index(arr, i) => {
                let vi = self.expr(i);
                let t = self.temp();
                self.emit(Tac::LoadA(t, arr.clone(), vi));
                Val::T(t)
            }
        }
    }

    /// Jumping code: go to `yes` if e is true, to `no` if it is false.
    fn cond(&mut self, e: &Expr, yes: u32, no: u32) {
        match &e.kind {
            ExprKind::Binary(BinOp::And, a, b) => {
                let mid = self.label();
                self.cond(a, mid, no); // a false: b is never evaluated
                self.emit(Tac::Label(mid));
                self.cond(b, yes, no);
            }
            ExprKind::Binary(BinOp::Or, a, b) => {
                let mid = self.label();
                self.cond(a, yes, mid); // a true: b is never evaluated
                self.emit(Tac::Label(mid));
                self.cond(b, yes, no);
            }
            ExprKind::Unary(UnOp::Not, a) => self.cond(a, no, yes),
            ExprKind::Binary(op, a, b) if relation(*op) => {
                let (va, vb) = (self.expr(a), self.expr(b));
                self.emit(Tac::Branch(*op, va, vb, yes));
                self.emit(Tac::Jump(no));
            }
            _ => {
                let v = self.expr(e);
                self.emit(Tac::Branch(BinOp::Ne, v, Val::K(0), yes));
                self.emit(Tac::Jump(no));
            }
        }
    }

    fn block(&mut self, b: &Block) {
        for s in &b.stmts {
            self.stmt(s);
        }
    }

    fn stmt(&mut self, s: &Stmt) {
        match &s.kind {
            StmtKind::Var(x, _, e) => {
                let v = self.expr(e);
                let t = self.declare(s.span.start, x);
                self.emit(Tac::Copy(t, v));
            }
            StmtKind::Assign(_, e) => {
                let v = self.expr(e);
                match self.place(s.span.start) {
                    Ok(t) => self.emit(Tac::Copy(t, v)),
                    Err(g) => self.emit(Tac::StoreG(g, v)),
                }
            }
            StmtKind::AssignIndex(arr, i, e) => {
                let (vi, v) = (self.expr(i), self.expr(e));
                self.emit(Tac::StoreA(arr.clone(), vi, v));
            }
            StmtKind::If(c, then, els) => {
                let (yes, no, end) = (self.label(), self.label(), self.label());
                self.cond(c, yes, no);
                self.emit(Tac::Label(yes));
                self.block(then);
                self.emit(Tac::Jump(end));
                self.emit(Tac::Label(no));
                if let Some(b) = els {
                    self.block(b);
                }
                self.emit(Tac::Label(end));
            }
            StmtKind::While(c, body) => {
                let (top, go, exit) = (self.label(), self.label(), self.label());
                self.emit(Tac::Label(top));
                self.cond(c, go, exit);
                self.emit(Tac::Label(go));
                self.block(body);
                self.emit(Tac::Jump(top));
                self.emit(Tac::Label(exit));
            }
            StmtKind::Return(e) => {
                let v = e.as_ref().map(|e| self.expr(e));
                self.emit(Tac::Ret(v));
            }
            StmtKind::Expr(Expr { kind: ExprKind::Call(f, args), .. }) => {
                let vs = args.iter().map(|a| self.expr(a)).collect();
                self.emit(Tac::Call(None, f.clone(), vs));
            }
            StmtKind::Expr(e) => { self.expr(e); }
            StmtKind::Block(b) => self.block(b),
        }
    }
}

fn relation(op: BinOp) -> bool {
    matches!(op, BinOp::Eq | BinOp::Ne | BinOp::Lt | BinOp::Le | BinOp::Gt | BinOp::Ge)
}

// ---- printing ---------------------------------------------------------------

pub fn val(f: &FuncTac, v: Val) -> String {
    match v {
        Val::K(n) => n.to_string(),
        Val::T(t) => f.names.get(&t).cloned().unwrap_or(format!("t{t}")),
    }
}

pub fn show(f: &FuncTac, i: &Tac) -> String {
    let v = |x: Val| val(f, x);
    let t = |x: u32| val(f, Val::T(x));
    match i {
        Tac::Bin(d, op, a, b) => format!("{} = {} {} {}", t(*d), v(*a), op.symbol(), v(*b)),
        Tac::Neg(d, a) => format!("{} = -{}", t(*d), v(*a)),
        Tac::Not(d, a) => format!("{} = !{}", t(*d), v(*a)),
        Tac::Copy(d, a) => format!("{} = {}", t(*d), v(*a)),
        Tac::LoadG(d, g) => format!("{} = {g}", t(*d)),
        Tac::StoreG(g, a) => format!("{g} = {}", v(*a)),
        Tac::LoadA(d, arr, i) => format!("{} = {arr}[{}]", t(*d), v(*i)),
        Tac::StoreA(arr, i, a) => format!("{arr}[{}] = {}", v(*i), v(*a)),
        Tac::Label(l) => format!("L{l}:"),
        Tac::Jump(l) => format!("goto L{l}"),
        Tac::Branch(op, a, b, l) => format!("if {} {} {} goto L{l}", v(*a), op.symbol(), v(*b)),
        Tac::Call(d, g, args) => {
            let a: Vec<String> = args.iter().map(|x| v(*x)).collect();
            let call = format!("call {g}({})", a.join(", "));
            match d { Some(d) => format!("{} = {call}", t(*d)), None => call }
        }
        Tac::Ret(Some(a)) => format!("return {}", v(*a)),
        Tac::Ret(None) => "return".into(),
    }
}
