// ex11_registers.rs -- exercise 11: the fewest registers that evaluate an
// expression tree without storing an intermediate result in memory.
#![allow(dead_code)]

pub enum E {
    Leaf,
    Op(Box<E>, Box<E>),
}

/// Sethi-Ullman (Ershov) number: a leaf needs 1; an operator needs the
/// larger of its children's needs, plus one if they are equal.
pub fn need(e: &E) -> u32 {
    match e {
        E::Leaf => 1,
        E::Op(a, b) => {
            let (x, y) = (need(a), need(b));
            if x == y { x + 1 } else { x.max(y) }
        }
    }
}

/// Registers used when the left operand is always evaluated first.
pub fn left_first(e: &E) -> u32 {
    match e {
        E::Leaf => 1,
        E::Op(a, b) => left_first(a).max(1 + left_first(b)),
    }
}
