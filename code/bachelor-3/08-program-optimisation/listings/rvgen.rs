// rvgen.rs -- instruction selection once temporaries have registers: an
// operand in a register is used in place; only spilled temporaries go
// through the stack. Registers are the callee-saved s0-s11.
#![allow(dead_code)]
use crate::ast::{BinOp, Expr, ExprKind, Item, Program, UnOp};
use crate::cfg;
use crate::regalloc::{colour, interference, spill_costs};
use crate::tac::{FuncTac, Tac, Val};
use std::collections::BTreeMap;

pub const REGS: [&str; 12] = [
    "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s0",
];

#[derive(Clone, Copy, PartialEq)]
pub enum Loc {
    Reg(&'static str),
    Slot(i32),
}

struct Gen<'a> {
    lines: Vec<String>,
    f: &'a FuncTac,
    loc: BTreeMap<u32, Loc>,
}

fn fits12(n: i32) -> bool {
    (-2048..=2047).contains(&n)
}

impl Gen<'_> {
    fn i(&mut self, s: String) {
        self.lines.push(format!("    {s}"));
    }
    /// The register holding v, loading it into `scratch` if needed.
    fn get(&mut self, v: Val, scratch: &'static str) -> &'static str {
        match v {
            Val::K(0) => "zero",
            Val::K(n) => {
                self.i(format!("li {scratch}, {n}"));
                scratch
            }
            Val::T(t) => match self.loc[&t] {
                Loc::Reg(r) => r,
                Loc::Slot(o) => {
                    self.i(format!("lw {scratch}, {o}(sp)"));
                    scratch
                }
            },
        }
    }
    /// Where to compute t: its register, or t0 before a store.
    fn target(&self, t: u32) -> &'static str {
        match self.loc[&t] {
            Loc::Reg(r) => r,
            Loc::Slot(_) => "t0",
        }
    }
    fn finish(&mut self, t: u32, reg: &str) {
        if let Loc::Slot(o) = self.loc[&t] {
            self.i(format!("sw {reg}, {o}(sp)"));
        }
    }
    fn mv(&mut self, to: &str, from: &str) {
        if to != from {
            self.i(format!("mv {to}, {from}"));
        }
    }
    fn label(&self, l: u32) -> String {
        format!(".L{}_{l}", self.f.name)
    }

    fn bin(&mut self, d: u32, op: BinOp, a: Val, b: Val) {
        use BinOp::*;
        let ra = self.get(a, "t0");
        let rd = self.target(d);
        match (op, b) {
            (Add, Val::K(n)) if fits12(n) => self.i(format!("addi {rd}, {ra}, {n}")),
            (Sub, Val::K(n)) if fits12(-n) => self.i(format!("addi {rd}, {ra}, {}", -n)),
            (Mul, Val::K(n)) if n > 0 && (n as u32).is_power_of_two() => {
                self.i(format!("slli {rd}, {ra}, {}", n.trailing_zeros()))
            }
            _ => {
                let rb = self.get(b, "t1");
                let ops: Vec<String> = match op {
                    Add => vec![format!("add {rd}, {ra}, {rb}")],
                    Sub => vec![format!("sub {rd}, {ra}, {rb}")],
                    Mul => vec![format!("mul {rd}, {ra}, {rb}")],
                    Div => vec![format!("div {rd}, {ra}, {rb}")],
                    Rem => vec![format!("rem {rd}, {ra}, {rb}")],
                    Lt => vec![format!("slt {rd}, {ra}, {rb}")],
                    Gt => vec![format!("slt {rd}, {rb}, {ra}")],
                    Le => vec![
                        format!("slt {rd}, {rb}, {ra}"),
                        format!("xori {rd}, {rd}, 1"),
                    ],
                    Ge => vec![
                        format!("slt {rd}, {ra}, {rb}"),
                        format!("xori {rd}, {rd}, 1"),
                    ],
                    Eq => vec![format!("xor {rd}, {ra}, {rb}"), format!("seqz {rd}, {rd}")],
                    Ne => vec![format!("xor {rd}, {ra}, {rb}"), format!("snez {rd}, {rd}")],
                    And | Or => unreachable!("jumping code"),
                };
                for s in ops {
                    self.i(s);
                }
            }
        }
        self.finish(d, rd);
    }

    fn element(&mut self, arr: &str, i: Val) {
        let ri = self.get(i, "t1");
        self.i(format!("slli t1, {ri}, 2"));
        self.i(format!("la t2, {arr}"));
        self.i("add t2, t2, t1".into());
    }

    fn instr(&mut self, ins: &Tac) {
        match ins {
            Tac::Bin(d, op, a, b) => self.bin(*d, *op, *a, *b),
            Tac::Neg(d, a) | Tac::Not(d, a) => {
                let (ra, rd) = (self.get(*a, "t0"), self.target(*d));
                let s = if matches!(ins, Tac::Neg(..)) {
                    format!("neg {rd}, {ra}")
                } else {
                    format!("xori {rd}, {ra}, 1")
                };
                self.i(s);
                self.finish(*d, rd);
            }
            Tac::Copy(d, Val::K(n)) => {
                let rd = self.target(*d);
                self.i(format!("li {rd}, {n}"));
                self.finish(*d, rd);
            }
            Tac::Copy(d, a) => {
                let ra = self.get(*a, "t0");
                match self.loc[d] {
                    Loc::Reg(r) => self.mv(r, ra),
                    Loc::Slot(o) => self.i(format!("sw {ra}, {o}(sp)")),
                }
            }
            Tac::LoadG(d, g) => {
                let rd = self.target(*d);
                self.i(format!("la t2, {g}"));
                self.i(format!("lw {rd}, 0(t2)"));
                self.finish(*d, rd);
            }
            Tac::StoreG(g, a) => {
                let ra = self.get(*a, "t0");
                self.i(format!("la t2, {g}"));
                self.i(format!("sw {ra}, 0(t2)"));
            }
            Tac::LoadA(d, arr, i) => {
                self.element(arr, *i);
                let rd = self.target(*d);
                self.i(format!("lw {rd}, 0(t2)"));
                self.finish(*d, rd);
            }
            Tac::StoreA(arr, i, a) => {
                self.element(arr, *i);
                let ra = self.get(*a, "t0");
                self.i(format!("sw {ra}, 0(t2)"));
            }
            Tac::Label(l) => self.lines.push(format!("{}:", self.label(*l))),
            Tac::Jump(l) => self.i(format!("j {}", self.label(*l))),
            Tac::Branch(op, a, b, l) => {
                let (x, y) = (self.get(*a, "t0"), self.get(*b, "t1"));
                let (m, x, y) = match op {
                    BinOp::Lt => ("blt", x, y),
                    BinOp::Ge => ("bge", x, y),
                    BinOp::Gt => ("blt", y, x),
                    BinOp::Le => ("bge", y, x),
                    BinOp::Eq => ("beq", x, y),
                    _ => ("bne", x, y),
                };
                self.i(format!("{m} {x}, {y}, {}", self.label(*l)));
            }
            Tac::Call(d, g, args) => {
                for (k, a) in args.iter().enumerate() {
                    let ak = ["a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"][k];
                    match a {
                        Val::K(n) => self.i(format!("li {ak}, {n}")),
                        Val::T(_) => {
                            let r = self.get(*a, ak);
                            self.mv(ak, r)
                        }
                    }
                }
                let body: Vec<String> = match g.as_str() {
                    "print" => ["li a7, 1", "ecall", "li a0, 10", "li a7, 11", "ecall"]
                        .map(String::from)
                        .to_vec(),
                    "print_char" => vec!["li a7, 11".into(), "ecall".into()],
                    "read" => vec!["li a7, 5".into(), "ecall".into()],
                    _ => vec![format!("call {g}")],
                };
                for s in body {
                    self.i(s);
                }
                if let Some(d) = d {
                    match self.loc[d] {
                        Loc::Reg(r) => self.mv(r, "a0"),
                        Loc::Slot(o) => self.i(format!("sw a0, {o}(sp)")),
                    }
                }
            }
            Tac::Ret(v) => {
                match v {
                    Some(Val::K(n)) => self.i(format!("li a0, {n}")),
                    Some(a) => {
                        let r = self.get(*a, "a0");
                        self.mv("a0", r)
                    }
                    None => self.i("li a0, 0".into()),
                }
                self.i(format!("j .L{}_ret", self.f.name));
            }
        }
    }
}

pub struct Report {
    pub registers: usize,
    pub spilled: usize,
    pub frame: i32,
}

/// One function with k registers: allocation, frame, prologue, body, epilogue.
pub fn function(f: &FuncTac, k: usize) -> (Vec<String>, Report) {
    let g = cfg::build(f);
    let gr = interference(f, &g);
    let c = colour(&gr, k.min(REGS.len()), &spill_costs(f, &g));
    let mut loc = BTreeMap::new();
    let mut used: Vec<&'static str> = vec![];
    for (&t, &col) in &c.colour {
        loc.insert(t, Loc::Reg(REGS[col]));
        if !used.contains(&REGS[col]) {
            used.push(REGS[col]);
        }
    }
    used.sort_by_key(|r| REGS.iter().position(|x| x == r));
    for (n, &t) in c.spilled.iter().enumerate() {
        loc.insert(t, Loc::Slot(4 * n as i32));
    }
    let builtin = |g: &str| ["print", "print_char", "read"].contains(&g);
    let calls = f.code.iter().any(|i| matches!(i, Tac::Call(_, g, _) if !builtin(g)));
    let saved = 4 * (c.spilled.len() + used.len() + calls as usize) as i32;
    let size = (saved + 15) / 16 * 16;
    let mut gen = Gen {
        lines: vec![format!("{}:", f.name)],
        f,
        loc,
    };
    let mut restore = vec![];
    if size > 0 {
        gen.i(format!("addi sp, sp, -{size}"));
        let mut off = 4 * c.spilled.len() as i32;
        for r in used.iter().copied().chain(calls.then_some("ra")) {
            gen.i(format!("sw {r}, {off}(sp)"));
            restore.push(format!("lw {r}, {off}(sp)"));
            off += 4;
        }
    }
    for (n, p) in f.params.iter().enumerate() {
        let an = ["a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"][n];
        match gen.loc.get(p) {
            Some(Loc::Reg(r)) => gen.mv(r, an),
            Some(Loc::Slot(o)) => {
                let o = *o;
                gen.i(format!("sw {an}, {o}(sp)"))
            }
            None => {} // a parameter never used
        }
    }
    for ins in &f.code {
        gen.instr(ins);
    }
    if gen.lines.last() == Some(&format!("    j .L{}_ret", f.name)) {
        gen.lines.pop(); // the epilogue follows
    }
    gen.lines.push(format!(".L{}_ret:", f.name));
    for r in restore {
        gen.i(r);
    }
    if size > 0 {
        gen.i(format!("addi sp, sp, {size}"));
    }
    gen.i("ret".into());
    let report = Report {
        registers: used.len(),
        spilled: c.spilled.len(),
        frame: size,
    };
    (gen.lines, report)
}

fn literal(e: &Expr) -> i32 {
    match &e.kind {
        ExprKind::Int(n) => *n as i32,
        ExprKind::Bool(b) => *b as i32,
        ExprKind::Unary(UnOp::Neg, a) => literal(a).wrapping_neg(),
        _ => 0,
    }
}

pub fn program(p: &Program, funcs: &[FuncTac], k: usize) -> (String, Vec<Report>) {
    let mut out = vec![".data".to_string()];
    for item in &p.items {
        match item {
            Item::Global { name, init, .. } => {
                out.push(format!(
                    "{name}: .word {}",
                    init.as_ref().map_or(0, literal)
                ));
            }
            Item::Array { name, size, .. } => out.push(format!("{name}: .space {}", 4 * size)),
            Item::Func(_) => {}
        }
    }
    out.push(".text".into());
    let mut reports = vec![];
    for f in funcs {
        let (lines, r) = function(f, k);
        out.extend(lines);
        reports.push(r);
    }
    (out.join("\n") + "\n", reports)
}
