// riscv.rs -- instruction selection for the rv subset: each three-address
// instruction becomes a few RISC-V instructions, every temporary living in
// its stack slot (no register allocation yet).
#![allow(dead_code)]
use crate::ast::{BinOp, Expr, ExprKind, Item, Program, UnOp};
use crate::frame::Frame;
use crate::tac::{FuncTac, Tac, Val};

/// A hook that may select instructions for a TAC instruction first.
pub type Extra<'a> = &'a dyn Fn(&Tac, &Frame, &mut Vec<String>) -> bool;

pub struct Asm<'a> {
    pub lines: Vec<String>,
    f: &'a FuncTac,
    frame: Frame,
}

fn fits12(n: i32) -> bool {
    (-2048..=2047).contains(&n)
}

impl Asm<'_> {
    fn i(&mut self, s: String) {
        self.lines.push(format!("    {s}"));
    }
    /// Put a value in a register: a load from its slot, or li.
    fn load(&mut self, v: Val, reg: &str) {
        match v {
            Val::T(t) => { let o = self.frame.slot(t); self.i(format!("lw {reg}, {o}(sp)")) }
            Val::K(n) => self.i(format!("li {reg}, {n}")),
        }
    }
    fn store(&mut self, t: u32, reg: &str) {
        let o = self.frame.slot(t);
        self.i(format!("sw {reg}, {o}(sp)"));
    }
    fn label(&self, l: u32) -> String {
        format!(".L{}_{l}", self.f.name)
    }

    fn bin(&mut self, d: u32, op: BinOp, a: Val, b: Val) -> Result<(), String> {
        use BinOp::*;
        self.load(a, "t0");
        match (op, b) {
            (Add, Val::K(n)) if fits12(n) => self.i(format!("addi t0, t0, {n}")),
            (Sub, Val::K(n)) if fits12(-n) => self.i(format!("addi t0, t0, {}", -n)),
            _ => {
                self.load(b, "t1");
                let ops: &[&str] = match op {
                    Add => &["add t0, t0, t1"], Sub => &["sub t0, t0, t1"],
                    Mul => &["mul t0, t0, t1"], Div => &["div t0, t0, t1"],
                    Lt => &["slt t0, t0, t1"], Gt => &["slt t0, t1, t0"],
                    Le => &["slt t0, t1, t0", "xori t0, t0, 1"],
                    Ge => &["slt t0, t0, t1", "xori t0, t0, 1"],
                    Eq => &["xor t0, t0, t1", "seqz t0, t0"],
                    Ne => &["xor t0, t0, t1", "snez t0, t0"],
                    Rem => return Err("no instructions selected for '%' (exercise 6)".into()),
                    And | Or => unreachable!("translated as jumps"),
                };
                for s in ops {
                    self.i(s.to_string());
                }
            }
        }
        self.store(d, "t0");
        Ok(())
    }

    fn instr(&mut self, ins: &Tac) -> Result<(), String> {
        match ins {
            Tac::Bin(d, op, a, b) => self.bin(*d, *op, *a, *b)?,
            Tac::Neg(..) => return Err("no instructions selected for '-x' (exercise 6)".into()),
            Tac::Not(d, a) => {
                self.load(*a, "t0");
                self.i("xori t0, t0, 1".into());
                self.store(*d, "t0");
            }
            Tac::Copy(d, a) => {
                self.load(*a, "t0");
                self.store(*d, "t0");
            }
            Tac::LoadG(d, g) => {
                self.i(format!("la t2, {g}"));
                self.i("lw t0, 0(t2)".into());
                self.store(*d, "t0");
            }
            Tac::StoreG(g, a) => {
                self.load(*a, "t0");
                self.i(format!("la t2, {g}"));
                self.i("sw t0, 0(t2)".into());
            }
            Tac::LoadA(d, arr, i) => {
                self.element(arr, *i);
                self.i("lw t0, 0(t2)".into());
                self.store(*d, "t0");
            }
            Tac::StoreA(arr, i, a) => {
                self.element(arr, *i);
                self.load(*a, "t0");
                self.i("sw t0, 0(t2)".into());
            }
            Tac::Label(l) => self.lines.push(format!("{}:", self.label(*l))),
            Tac::Jump(l) => self.i(format!("j {}", self.label(*l))),
            Tac::Branch(op, a, b, l) => {
                self.load(*a, "t0");
                self.load(*b, "t1");
                let (m, x, y) = match op {
                    BinOp::Lt => ("blt", "t0", "t1"), BinOp::Ge => ("bge", "t0", "t1"),
                    BinOp::Gt => ("blt", "t1", "t0"), BinOp::Le => ("bge", "t1", "t0"),
                    BinOp::Eq => ("beq", "t0", "t1"), _ => ("bne", "t0", "t1"),
                };
                self.i(format!("{m} {x}, {y}, {}", self.label(*l)));
            }
            Tac::Call(d, g, args) => self.call(*d, g, args)?,
            Tac::Ret(v) => {
                self.load(v.unwrap_or(Val::K(0)), "a0");
                self.i(format!("j .L{}_ret", self.f.name));
            }
        }
        Ok(())
    }

    /// t2 = the address of arr[i].
    fn element(&mut self, arr: &str, i: Val) {
        self.load(i, "t1");
        self.i("slli t1, t1, 2".into());
        self.i(format!("la t2, {arr}"));
        self.i("add t2, t2, t1".into());
    }

    fn call(&mut self, d: Option<u32>, g: &str, args: &[Val]) -> Result<(), String> {
        if args.len() > 8 {
            return Err(format!("{g}: more than 8 arguments"));
        }
        for (k, a) in args.iter().enumerate() {
            self.load(*a, &format!("a{k}"));
        }
        match g {
            "print" => {
                for s in ["li a7, 1", "ecall", "li a0, 10", "li a7, 11", "ecall"] {
                    self.i(s.into());
                }
            }
            "print_char" => { self.i("li a7, 11".into()); self.i("ecall".into()) }
            "read" => { self.i("li a7, 5".into()); self.i("ecall".into()) }
            _ => self.i(format!("call {g}")),
        }
        if let Some(d) = d {
            self.store(d, "a0");
        }
        Ok(())
    }
}

/// One function: prologue, body, epilogue.
pub fn function(f: &FuncTac, extra: Option<Extra>) -> Result<Vec<String>, String> {
    let frame = Frame::new(f.temps);
    let mut a = Asm { lines: vec![format!("{}:", f.name)], f, frame };
    a.i(format!("addi sp, sp, -{}", frame.size));
    a.i(format!("sw ra, {}(sp)", frame.ra));
    for (k, p) in f.params.iter().enumerate() {
        a.store(*p, &format!("a{k}"));
    }
    for ins in &f.code {
        if let Some(x) = extra {
            if x(ins, &frame, &mut a.lines) {
                continue;
            }
        }
        a.instr(ins)?;
    }
    a.lines.push(format!(".L{}_ret:", f.name));
    a.i(format!("lw ra, {}(sp)", frame.ra));
    a.i(format!("addi sp, sp, {}", frame.size));
    a.i("ret".into());
    Ok(a.lines)
}

/// The whole program: globals and arrays in .data, functions in .text.
pub fn program(p: &Program, funcs: &[FuncTac], extra: Option<Extra>) -> Result<String, String> {
    let mut out = vec![".data".to_string()];
    for item in &p.items {
        match item {
            Item::Global { name, init, .. } => {
                let v = init.as_ref().map_or(0, literal);
                out.push(format!("{name}: .word {v}"));
            }
            Item::Array { name, size, .. } => out.push(format!("{name}: .space {}", 4 * size)),
            Item::Func(_) => {}
        }
    }
    out.push(".text".into());
    for f in funcs {
        out.extend(function(f, extra)?);
    }
    Ok(out.join("\n") + "\n")
}

/// A global's initialiser: a literal, possibly negated.
fn literal(e: &Expr) -> i32 {
    match &e.kind {
        ExprKind::Int(n) => *n as i32,
        ExprKind::Bool(b) => *b as i32,
        ExprKind::Unary(UnOp::Neg, a) => literal(a).wrapping_neg(),
        _ => 0,
    }
}
