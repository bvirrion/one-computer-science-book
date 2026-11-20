// ast.rs -- the abstract syntax tree of Moor. Frozen for the book.
#![allow(dead_code)]
use crate::token::Span;
use std::fmt;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Type { Int, Bool }

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum BinOp { Add, Sub, Mul, Div, Rem, Eq, Ne, Lt, Le, Gt, Ge, And, Or }

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum UnOp { Neg, Not }

#[derive(Clone, Debug, PartialEq)]
pub enum ExprKind {
    Int(i64),
    Bool(bool),
    Var(String),
    Unary(UnOp, Box<Expr>),
    Binary(BinOp, Box<Expr>, Box<Expr>),
    Call(String, Vec<Expr>),
    Index(String, Box<Expr>), // a[e]: arrays are global and named
}

#[derive(Clone, Debug, PartialEq)]
pub struct Expr {
    pub kind: ExprKind,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub enum StmtKind {
    Var(String, Option<Type>, Expr), // var x [: T] = e;
    Assign(String, Expr),            // x = e;
    AssignIndex(String, Expr, Expr), // a[i] = e;
    If(Expr, Block, Option<Block>),  // else if ... is an else block holding one if
    While(Expr, Block),
    Return(Option<Expr>),
    Expr(Expr),
    Block(Block),
}

#[derive(Clone, Debug, PartialEq)]
pub struct Stmt {
    pub kind: StmtKind,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Block {
    pub stmts: Vec<Stmt>,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Param {
    pub name: String,
    pub ty: Type,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Func {
    pub name: String,
    pub params: Vec<Param>,
    pub ret: Option<Type>,
    pub body: Block,
    pub span: Span,
}

#[derive(Clone, Debug, PartialEq)]
pub enum Item {
    Func(Func),
    Global { name: String, ty: Type, init: Option<Expr>, span: Span }, // init: a literal
    Array { name: String, size: i64, span: Span },
}

#[derive(Clone, Debug, PartialEq, Default)]
pub struct Program {
    pub items: Vec<Item>,
}

impl BinOp {
    pub fn symbol(self) -> &'static str {
        use BinOp::*;
        match self {
            Add => "+", Sub => "-", Mul => "*", Div => "/", Rem => "%", Eq => "==", Ne => "!=",
            Lt => "<", Le => "<=", Gt => ">", Ge => ">=", And => "&&", Or => "||",
        }
    }
}

impl fmt::Display for Type {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.write_str(match self { Type::Int => "int", Type::Bool => "bool" })
    }
}

/// An expression as an S-expression: (+ a (* b c)).
impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &self.kind {
            ExprKind::Int(v) => write!(f, "{v}"),
            ExprKind::Bool(b) => write!(f, "{b}"),
            ExprKind::Var(x) => write!(f, "{x}"),
            ExprKind::Unary(UnOp::Neg, e) => write!(f, "(neg {e})"),
            ExprKind::Unary(UnOp::Not, e) => write!(f, "(! {e})"),
            ExprKind::Binary(op, a, b) => write!(f, "({} {a} {b})", op.symbol()),
            ExprKind::Call(g, args) => {
                write!(f, "(call {g}")?;
                for a in args {
                    write!(f, " {a}")?;
                }
                write!(f, ")")
            }
            ExprKind::Index(a, i) => write!(f, "(index {a} {i})"),
        }
    }
}

/// A whole program, one statement per line, indented by nesting.
pub fn pretty(p: &Program) -> String {
    let mut out = String::new();
    for item in &p.items {
        match item {
            Item::Func(func) => {
                let params: Vec<String> = func.params.iter().map(|q| format!("{}: {}", q.name, q.ty)).collect();
                let ret = func.ret.map_or(String::new(), |t| format!(" -> {t}"));
                out += &format!("fn {}({}){}\n", func.name, params.join(", "), ret);
                block(&func.body, 1, &mut out);
            }
            Item::Global { name, ty, init, .. } => {
                let init = init.as_ref().map_or(String::new(), |e| format!(" = {e}"));
                out += &format!("global {name}: {ty}{init}\n");
            }
            Item::Array { name, size, .. } => out += &format!("array {name}[{size}]\n"),
        }
    }
    out
}

fn block(b: &Block, depth: usize, out: &mut String) {
    for s in &b.stmts {
        stmt(s, depth, out);
    }
}

fn stmt(s: &Stmt, depth: usize, out: &mut String) {
    let pad = "  ".repeat(depth);
    match &s.kind {
        StmtKind::Var(x, t, e) => {
            let t = t.map_or(String::new(), |t| format!(": {t}"));
            *out += &format!("{pad}var {x}{t} = {e}\n");
        }
        StmtKind::Assign(x, e) => *out += &format!("{pad}{x} = {e}\n"),
        StmtKind::AssignIndex(a, i, e) => *out += &format!("{pad}{a}[{i}] = {e}\n"),
        StmtKind::If(c, then, other) => {
            *out += &format!("{pad}if {c}\n");
            block(then, depth + 1, out);
            if let Some(o) = other {
                *out += &format!("{pad}else\n");
                block(o, depth + 1, out);
            }
        }
        StmtKind::While(c, body) => {
            *out += &format!("{pad}while {c}\n");
            block(body, depth + 1, out);
        }
        StmtKind::Return(e) => match e {
            Some(e) => *out += &format!("{pad}return {e}\n"),
            None => *out += &format!("{pad}return\n"),
        },
        StmtKind::Expr(e) => *out += &format!("{pad}{e}\n"),
        StmtKind::Block(b) => {
            *out += &format!("{pad}block\n");
            block(b, depth + 1, out);
        }
    }
}
