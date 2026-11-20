// interp.rs -- a tree-walking interpreter for Moor: the reference meaning
// of a program, which the compiled code must reproduce. Integers are 32-bit
// and wrap, and division follows RISC-V. Frozen for the book.
#![allow(dead_code)]
use crate::ast::*;
use std::collections::HashMap;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum V { Int(i32), Bool(bool), Unit }

pub struct Outcome {
    pub output: String,
    pub exit: Result<i32, String>, // exit status, or the runtime error
    pub steps: u64,                // statements executed
}

enum Flow { Next, Ret(V) }
type R<X> = Result<X, String>;

struct Interp<'p> {
    funcs: HashMap<&'p str, &'p Func>,
    globals: HashMap<String, V>,
    arrays: HashMap<String, Vec<i32>>,
    frames: Vec<Vec<HashMap<String, V>>>, // per call, a stack of block scopes
    input: Vec<i32>,
    out: String,
    steps: u64,
    fuel: u64,
}

pub fn run(p: &Program, input: &[i32], fuel: u64) -> Outcome {
    let mut it = Interp { funcs: HashMap::new(), globals: HashMap::new(), arrays: HashMap::new(),
                          frames: vec![], input: input.iter().rev().copied().collect(),
                          out: String::new(), steps: 0, fuel };
    for item in &p.items {
        match item {
            Item::Func(f) => {
                it.funcs.insert(&f.name, f);
            }
            Item::Global { name, ty, init, .. } => {
                let v = match (init, ty) {
                    (Some(e), _) => literal(e),
                    (None, Type::Int) => V::Int(0),
                    (None, Type::Bool) => V::Bool(false),
                };
                it.globals.insert(name.clone(), v);
            }
            Item::Array { name, size, .. } => {
                it.arrays.insert(name.clone(), vec![0; *size as usize]);
            }
        }
    }
    let exit = it.call("main", vec![]).map(|v| if let V::Int(n) = v { n & 0xff } else { 0 });
    Outcome { output: it.out, exit, steps: it.steps }
}

fn literal(e: &Expr) -> V {
    match &e.kind {
        ExprKind::Int(n) => V::Int(*n as i32),
        ExprKind::Bool(b) => V::Bool(*b),
        ExprKind::Unary(UnOp::Neg, a) => match literal(a) { V::Int(n) => V::Int(n.wrapping_neg()), v => v },
        _ => V::Unit,
    }
}

impl<'p> Interp<'p> {
    fn call(&mut self, name: &str, args: Vec<V>) -> R<V> {
        match name {
            "print" => {
                self.out += &format!("{}\n", int(args[0]));
                return Ok(V::Unit);
            }
            "print_char" => {
                self.out.push((int(args[0]) & 0xff) as u8 as char);
                return Ok(V::Unit);
            }
            "read" => return self.input.pop().map(V::Int).ok_or("read: no more input".to_string()),
            _ => {}
        }
        if self.frames.len() >= 1000 {
            return Err("calls nested more than 1000 deep".into());
        }
        let f = self.funcs[name];
        let scope = f.params.iter().map(|q| q.name.clone()).zip(args).collect();
        self.frames.push(vec![scope]);
        let flow = self.block(&f.body);
        self.frames.pop();
        Ok(match flow? { Flow::Ret(v) => v, Flow::Next => V::Unit })
    }

    fn block(&mut self, b: &'p Block) -> R<Flow> {
        self.frames.last_mut().unwrap().push(HashMap::new());
        let mut flow = Ok(Flow::Next);
        for s in &b.stmts {
            flow = self.stmt(s);
            if !matches!(flow, Ok(Flow::Next)) {
                break;
            }
        }
        self.frames.last_mut().unwrap().pop();
        flow
    }

    fn stmt(&mut self, s: &'p Stmt) -> R<Flow> {
        self.steps += 1;
        if self.steps > self.fuel {
            return Err(format!("stopped after {} statements", self.fuel));
        }
        match &s.kind {
            StmtKind::Var(x, _, e) => {
                let v = self.expr(e)?;
                let scopes = self.frames.last_mut().unwrap();
                scopes.last_mut().unwrap().insert(x.clone(), v);
            }
            StmtKind::Assign(x, e) => {
                let v = self.expr(e)?;
                *self.var(x) = v;
            }
            StmtKind::AssignIndex(a, i, e) => {
                let i = int(self.expr(i)?);
                let v = int(self.expr(e)?);
                *self.cell(a, i)? = v;
            }
            StmtKind::If(c, t, f) => {
                if self.expr(c)? == V::Bool(true) {
                    return self.block(t);
                } else if let Some(f) = f {
                    return self.block(f);
                }
            }
            StmtKind::While(c, b) => {
                while self.expr(c)? == V::Bool(true) {
                    if let Flow::Ret(v) = self.block(b)? {
                        return Ok(Flow::Ret(v));
                    }
                }
            }
            StmtKind::Return(e) => {
                let v = match e { Some(e) => self.expr(e)?, None => V::Unit };
                return Ok(Flow::Ret(v));
            }
            StmtKind::Expr(e) => {
                self.expr(e)?;
            }
            StmtKind::Block(b) => return self.block(b),
        }
        Ok(Flow::Next)
    }

    /// The innermost local of that name in the current call, else the global.
    fn var(&mut self, x: &str) -> &mut V {
        let scopes = self.frames.last_mut().unwrap();
        match scopes.iter_mut().rev().find(|s| s.contains_key(x)) {
            Some(s) => s.get_mut(x).unwrap(),
            None => self.globals.get_mut(x).unwrap(),
        }
    }
    fn cell(&mut self, a: &str, i: i32) -> R<&mut i32> {
        let arr = self.arrays.get_mut(a).unwrap();
        let n = arr.len();
        arr.get_mut(i as usize).filter(|_| i >= 0)
            .ok_or(format!("index {i} is out of range for '{a}', of size {n}"))
    }

    fn expr(&mut self, e: &'p Expr) -> R<V> {
        Ok(match &e.kind {
            ExprKind::Int(n) => V::Int(*n as i32),
            ExprKind::Bool(b) => V::Bool(*b),
            ExprKind::Var(x) => *self.var(x),
            ExprKind::Unary(UnOp::Neg, a) => V::Int(int(self.expr(a)?).wrapping_neg()),
            ExprKind::Unary(UnOp::Not, a) => V::Bool(!boolean(self.expr(a)?)),
            ExprKind::Binary(BinOp::And, a, b) => V::Bool(boolean(self.expr(a)?) && boolean(self.expr(b)?)),
            ExprKind::Binary(BinOp::Or, a, b) => V::Bool(boolean(self.expr(a)?) || boolean(self.expr(b)?)),
            ExprKind::Binary(op, a, b) => {
                let (x, y) = (self.expr(a)?, self.expr(b)?);
                binary(*op, x, y)
            }
            ExprKind::Call(f, args) => {
                let mut vs = Vec::new();
                for a in args {
                    vs.push(self.expr(a)?);
                }
                self.call(f, vs)?
            }
            ExprKind::Index(a, i) => {
                let i = int(self.expr(i)?);
                V::Int(*self.cell(a, i)?)
            }
        })
    }
}

fn int(v: V) -> i32 {
    if let V::Int(n) = v { n } else { unreachable!("a checked program") }
}
fn boolean(v: V) -> bool {
    if let V::Bool(b) = v { b } else { unreachable!("a checked program") }
}

/// The operators on 32-bit values, as RISC-V computes them.
pub fn binary(op: BinOp, x: V, y: V) -> V {
    use BinOp::*;
    if let (Eq | Ne, V::Bool(a), V::Bool(b)) = (op, x, y) {
        return V::Bool((a == b) == (op == Eq));
    }
    let (a, b) = (int(x), int(y));
    match op {
        Add => V::Int(a.wrapping_add(b)),
        Sub => V::Int(a.wrapping_sub(b)),
        Mul => V::Int(a.wrapping_mul(b)),
        Div => V::Int(if b == 0 { -1 } else { a.wrapping_div(b) }),
        Rem => V::Int(if b == 0 { a } else { a.wrapping_rem(b) }),
        Eq => V::Bool(a == b),
        Ne => V::Bool(a != b),
        Lt => V::Bool(a < b),
        Le => V::Bool(a <= b),
        Gt => V::Bool(a > b),
        Ge => V::Bool(a >= b),
        And | Or => unreachable!("short-circuit, handled by the caller"),
    }
}
