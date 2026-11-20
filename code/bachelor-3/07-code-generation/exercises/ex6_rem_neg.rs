// ex6_rem_neg.rs -- exercise 6: instructions for '%' and unary '-',
// plugged into riscv::function as an extra selection hook.
#![allow(dead_code)]
use crate::ast::BinOp;
use crate::frame::Frame;
use crate::tac::{Tac, Val};

fn load(v: Val, reg: &str, fr: &Frame, out: &mut Vec<String>) {
    out.push(match v {
        Val::T(t) => format!("    lw {reg}, {}(sp)", fr.slot(t)),
        Val::K(n) => format!("    li {reg}, {n}"),
    });
}

pub fn select(ins: &Tac, fr: &Frame, out: &mut Vec<String>) -> bool {
    match ins {
        Tac::Bin(d, BinOp::Rem, a, b) => {
            load(*a, "t0", fr, out);
            load(*b, "t1", fr, out);
            out.push("    rem t0, t0, t1".into()); // RISC-V rem: the interpreter's rule
            out.push(format!("    sw t0, {}(sp)", fr.slot(*d)));
            true
        }
        Tac::Neg(d, a) => {
            load(*a, "t0", fr, out);
            out.push("    neg t0, t0".into()); // sub t0, zero, t0
            out.push(format!("    sw t0, {}(sp)", fr.slot(*d)));
            true
        }
        _ => false,
    }
}
