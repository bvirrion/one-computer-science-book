// expr.rs: arithmetic expressions in one variable x, as a recursive enum; integers modulo 2^64.
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Num(i64),
    X,
    Add(Box<Expr>, Box<Expr>), // a Box: the sub-expression lives on the heap
    Mul(Box<Expr>, Box<Expr>),
}
use Expr::*;

impl Expr {
    pub fn eval(&self, x: i64) -> i64 {
        match self {
            Num(n) => *n,
            X => x,
            Add(a, b) => a.eval(x).wrapping_add(b.eval(x)),
            Mul(a, b) => a.eval(x).wrapping_mul(b.eval(x)),
        }
    }

    pub fn simplify(self) -> Expr {
        match self {
            Add(a, b) => match (a.simplify(), b.simplify()) {
                (Num(m), Num(n)) => Num(m.wrapping_add(n)), // fold constants
                (Num(0), e) | (e, Num(0)) => e,             // 0 + e = e
                (a, b) => Add(Box::new(a), Box::new(b)),
            },
            Mul(a, b) => match (a.simplify(), b.simplify()) {
                (Num(m), Num(n)) => Num(m.wrapping_mul(n)),
                (Num(0), _) | (_, Num(0)) => Num(0),        // 0 * e = 0
                (Num(1), e) | (e, Num(1)) => e,             // 1 * e = e
                (a, b) => Mul(Box::new(a), Box::new(b)),
            },
            leaf => leaf, // Num and X are already simple
        }
    }
}

impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Num(n) => write!(f, "{n}"),
            X => write!(f, "x"),
            Add(a, b) => write!(f, "({a} + {b})"),
            Mul(a, b) => write!(f, "{a} * {b}"),
        }
    }
}

#[allow(dead_code)]
fn main() {
    let n = |k| Box::new(Num(k));
    // (x * (2 + -1) + 0) * (3 * x + 4 * 0)
    let e = Mul(
        Box::new(Add(Box::new(Mul(Box::new(X), Box::new(Add(n(2), n(-1))))), n(0))),
        Box::new(Add(Box::new(Mul(n(3), Box::new(X))), Box::new(Mul(n(4), n(0))))),
    );
    println!("{e}  at x = 5: {}", e.eval(5));
    let s = e.clone().simplify();
    println!("{s}  at x = 5: {}", s.eval(5));
}
