// resolve.rs -- name resolution for Moor: each use of a name bound to its
// declaration, in two passes. Frozen for the book.
#![allow(dead_code)]
use crate::ast::*;
use crate::scope::Scopes;
use crate::token::Span;
use std::collections::HashMap;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind { Local, Param, Global, Array, Func, Builtin }

#[derive(Clone, Debug)]
pub struct Decl {
    pub name: String,
    pub kind: Kind,
    pub span: Span,
}

/// A message, its place, and an optional note pointing somewhere else.
#[derive(Clone, Debug)]
pub struct Diag {
    pub msg: String,
    pub span: Span,
    pub note: Option<(String, Span)>,
}

pub const BUILTINS: [&str; 3] = ["print", "print_char", "read"];
pub const NOWHERE: Span = Span { start: 0, end: 0, line: 1, col: 1 };

/// The side tables: declarations by number, and for each use and each
/// declaring node (keyed by the byte where it starts) the declaration's number.
#[derive(Default)]
pub struct Resolution {
    pub decls: Vec<Decl>,
    pub uses: HashMap<usize, usize>,
    pub defs: HashMap<usize, usize>,
    pub items: Vec<usize>,
    pub errors: Vec<Diag>,
}

struct Resolver<'t> {
    r: Resolution,
    scopes: Scopes<usize>,
    later: Vec<(String, Span)>, // the current function's local declarations
    trace: &'t mut dyn FnMut(&str, &Scopes<usize>),
}

pub fn resolve(p: &Program) -> Resolution {
    resolve_traced(p, &mut |_, _| {})
}

/// Pass 1 declares every item, so functions may call each other in any
/// order; pass 2 walks each body with a scope per block.
pub fn resolve_traced(p: &Program, trace: &mut dyn FnMut(&str, &Scopes<usize>))
    -> Resolution {
    let mut rs = Resolver {
        r: Resolution::default(), scopes: Scopes::new(), later: vec![], trace,
    };
    for b in BUILTINS {
        rs.declare(b, Kind::Builtin, NOWHERE);
    }
    for item in &p.items {
        let id = match item {
            Item::Func(f) => rs.declare(&f.name, Kind::Func, f.span),
            Item::Global { name, span, .. } => rs.declare(name, Kind::Global, *span),
            Item::Array { name, span, .. } => rs.declare(name, Kind::Array, *span),
        };
        rs.r.items.push(id);
    }
    for item in &p.items {
        if let Item::Func(f) = item {
            rs.later.clear();
            collect_vars(&f.body, &mut rs.later);
            rs.scopes.push();
            for q in &f.params {
                let id = rs.declare(&q.name, Kind::Param, q.span);
                rs.r.defs.insert(q.span.start, id);
            }
            rs.block(&f.body);
            rs.scopes.pop();
        }
    }
    rs.r
}

impl Resolver<'_> {
    fn declare(&mut self, name: &str, kind: Kind, span: Span) -> usize {
        let id = self.r.decls.len();
        self.r.decls.push(Decl { name: name.to_string(), kind, span });
        if let Err(old) = self.scopes.declare(name, id) {
            let first = &self.r.decls[old];
            let (msg, note) = if first.kind == Kind::Builtin {
                (format!("'{name}' is the name of a built-in function"), None)
            } else {
                (format!("'{name}' is declared twice in the same scope"),
                 Some(("the first declaration is here".to_string(), first.span)))
            };
            self.r.errors.push(Diag { msg, span, note });
        }
        (self.trace)(name, &self.scopes);
        id
    }

    fn use_name(&mut self, name: &str, span: Span) {
        if let Some(id) = self.scopes.lookup(name) {
            self.r.uses.insert(span.start, id);
            return;
        }
        let msg;
        let mut note = None;
        let later = self.later.iter().find(|(x, at)| x == name && at.start > span.start);
        if let Some((_, at)) = later {
            msg = format!("'{name}' is used before its declaration");
            note = Some(("it is declared here".to_string(), *at));
        } else {
            msg = format!("'{name}' is not declared");
        }
        self.r.errors.push(Diag { msg, span, note });
    }

    fn block(&mut self, b: &Block) {
        self.scopes.push();
        for s in &b.stmts {
            self.stmt(s);
        }
        self.scopes.pop();
    }

    fn stmt(&mut self, s: &Stmt) {
        match &s.kind {
            StmtKind::Var(x, _, e) => {
                self.expr(e); // the initialiser cannot see the new name
                let id = self.declare(x, Kind::Local, s.span);
                self.r.defs.insert(s.span.start, id);
            }
            StmtKind::Assign(x, e) => {
                self.use_name(x, s.span);
                self.expr(e);
            }
            StmtKind::AssignIndex(a, i, e) => {
                self.use_name(a, s.span);
                self.expr(i);
                self.expr(e);
            }
            StmtKind::If(c, t, f) => {
                self.expr(c);
                self.block(t);
                if let Some(f) = f {
                    self.block(f);
                }
            }
            StmtKind::While(c, b) => {
                self.expr(c);
                self.block(b);
            }
            StmtKind::Return(e) => {
                if let Some(e) = e {
                    self.expr(e);
                }
            }
            StmtKind::Expr(e) => self.expr(e),
            StmtKind::Block(b) => self.block(b),
        }
    }

    fn expr(&mut self, e: &Expr) {
        match &e.kind {
            ExprKind::Int(_) | ExprKind::Bool(_) => {}
            ExprKind::Var(x) => self.use_name(x, e.span),
            ExprKind::Unary(_, a) => self.expr(a),
            ExprKind::Binary(_, a, b) => {
                self.expr(a);
                self.expr(b);
            }
            ExprKind::Call(f, args) => {
                self.use_name(f, e.span);
                for a in args {
                    self.expr(a);
                }
            }
            ExprKind::Index(a, i) => {
                self.use_name(a, e.span);
                self.expr(i);
            }
        }
    }
}

/// Every `var` of a block and its sub-blocks, with where it is.
fn collect_vars(b: &Block, out: &mut Vec<(String, Span)>) {
    for s in &b.stmts {
        match &s.kind {
            StmtKind::Var(x, _, _) => out.push((x.clone(), s.span)),
            StmtKind::If(_, t, f) => {
                collect_vars(t, out);
                if let Some(f) = f {
                    collect_vars(f, out);
                }
            }
            StmtKind::While(_, b) | StmtKind::Block(b) => collect_vars(b, out),
            _ => {}
        }
    }
}

/// An error with its source line and caret, and the note the same way.
pub fn render(src: &str, file: &str, d: &Diag) -> String {
    let err = crate::lexer::LexError { msg: d.msg.clone(), span: d.span };
    let mut out = crate::lexer::show_error(src, file, &err);
    if let Some((msg, span)) = &d.note {
        let note = crate::lexer::LexError { msg: msg.clone(), span: *span };
        out += &crate::lexer::show_error(src, file, &note).replacen(": error: ", ": note: ", 1);
    }
    out
}
