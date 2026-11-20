// pb_register.rs -- the weekend problem: generated register scripts, and
// the cost of resolving their names with three symbol tables.
#![allow(dead_code)]

/// d nested blocks, m declarations in each, every one initialised from the
/// register `reg`, declared first in the outermost block.
pub fn script(d: usize, m: usize, misspelt_block: Option<usize>) -> String {
    let mut s = String::from("fn main() {\n    var reg = 0;\n");
    for i in 1..=d {
        let pad = "    ".repeat(i);
        if i > 1 {
            s += &format!("{}{{\n", "    ".repeat(i - 1));
        }
        let name = if misspelt_block == Some(i) { "rge" } else { "reg" };
        for j in 1..=m {
            s += &format!("{pad}var v{i}_{j} = {name} + {j};\n");
        }
    }
    for i in (1..d).rev() {
        s += &format!("{}}}\n", "    ".repeat(i));
    }
    s += "}\n";
    s
}

/// A list of (name, declaration) pairs, newest last; a block remembers the
/// length of the list when it opened.
pub struct ListScopes {
    pairs: Vec<(String, usize)>,
    marks: Vec<usize>,
    pub comparisons: u64,
}

impl ListScopes {
    pub fn new() -> Self {
        ListScopes { pairs: vec![], marks: vec![], comparisons: 0 }
    }
    pub fn enter(&mut self) {
        self.marks.push(self.pairs.len());
    }
    pub fn exit(&mut self) {
        let k = self.marks.pop().unwrap();
        self.pairs.truncate(k);
    }
    pub fn declare(&mut self, name: &str, id: usize) {
        self.pairs.push((name.to_string(), id));
    }
    pub fn lookup(&mut self, name: &str) -> Option<usize> {
        for (x, id) in self.pairs.iter().rev() {
            self.comparisons += 1;
            if x == name {
                return Some(*id);
            }
        }
        None
    }
}

use crate::ast::*;

/// What a symbol table must offer to resolve the script.
pub trait Table {
    fn enter(&mut self);
    fn exit(&mut self);
    fn declare(&mut self, name: &str);
    fn lookup(&mut self, name: &str) -> bool;
}

impl Table for ListScopes {
    fn enter(&mut self) {
        ListScopes::enter(self)
    }
    fn exit(&mut self) {
        ListScopes::exit(self)
    }
    fn declare(&mut self, name: &str) {
        ListScopes::declare(self, name, 0)
    }
    fn lookup(&mut self, name: &str) -> bool {
        ListScopes::lookup(self, name).is_some()
    }
}

/// Resolve the names of a block with any table; returns the misses.
pub fn walk(b: &Block, t: &mut dyn Table) -> usize {
    let mut misses = 0;
    t.enter();
    for s in &b.stmts {
        match &s.kind {
            StmtKind::Var(x, _, e) => {
                misses += uses(e, t);
                t.declare(x);
            }
            StmtKind::Block(b) => misses += walk(b, t),
            _ => {}
        }
    }
    t.exit();
    misses
}

fn uses(e: &Expr, t: &mut dyn Table) -> usize {
    match &e.kind {
        ExprKind::Var(x) => !t.lookup(x) as usize,
        ExprKind::Binary(_, a, b) => uses(a, t) + uses(b, t),
        _ => 0,
    }
}
