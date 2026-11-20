// ex6_unused.rs -- exercise 6: a warning for every local variable or
// parameter that is never read (assigning to it does not count).
#![allow(dead_code)]
use crate::ast::*;
use crate::resolve::{Diag, Kind, Resolution};
use std::collections::HashSet;

pub fn unused(p: &Program, r: &Resolution) -> Vec<Diag> {
    let mut read = HashSet::new();
    for item in &p.items {
        if let Item::Func(f) = item {
            reads_block(&f.body, r, &mut read);
        }
    }
    let mut out: Vec<Diag> = r.decls.iter().enumerate()
        .filter(|(id, d)| matches!(d.kind, Kind::Local | Kind::Param) && !read.contains(id))
        .map(|(_, d)| Diag { msg: format!("'{}' is never read", d.name), span: d.span, note: None })
        .collect();
    out.sort_by_key(|d| d.span.start);
    out
}

fn reads_block(b: &Block, r: &Resolution, read: &mut HashSet<usize>) {
    for s in &b.stmts {
        match &s.kind {
            StmtKind::Var(_, _, e) | StmtKind::Assign(_, e) | StmtKind::Expr(e) => reads(e, r, read),
            StmtKind::Return(e) => {
                if let Some(e) = e {
                    reads(e, r, read);
                }
            }
            StmtKind::AssignIndex(_, i, e) => {
                reads(i, r, read);
                reads(e, r, read);
            }
            StmtKind::If(c, t, f) => {
                reads(c, r, read);
                reads_block(t, r, read);
                if let Some(f) = f {
                    reads_block(f, r, read);
                }
            }
            StmtKind::While(c, b) => {
                reads(c, r, read);
                reads_block(b, r, read);
            }
            StmtKind::Block(b) => reads_block(b, r, read),
        }
    }
}

fn reads(e: &Expr, r: &Resolution, read: &mut HashSet<usize>) {
    match &e.kind {
        ExprKind::Var(_) => {
            if let Some(&id) = r.uses.get(&e.span.start) {
                read.insert(id);
            }
        }
        ExprKind::Unary(_, a) => reads(a, r, read),
        ExprKind::Binary(_, a, b) => {
            reads(a, r, read);
            reads(b, r, read);
        }
        ExprKind::Call(_, args) => args.iter().for_each(|a| reads(a, r, read)),
        ExprKind::Index(_, i) => reads(i, r, read),
        ExprKind::Int(_) | ExprKind::Bool(_) => {}
    }
}
