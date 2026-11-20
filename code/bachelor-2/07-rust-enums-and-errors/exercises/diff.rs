// diff.rs: symbolic differentiation with simplification (exercise 10).
#[derive(Debug, Clone, PartialEq)]
pub enum F {
    Num(f64),
    X,
    Add(Box<F>, Box<F>),
    Mul(Box<F>, Box<F>),
    Sin(Box<F>),
    Cos(Box<F>),
}
use F::*;

fn b(f: F) -> Box<F> {
    Box::new(f)
}

impl F {
    pub fn eval(&self, x: f64) -> f64 {
        match self {
            Num(c) => *c,
            X => x,
            Add(p, q) => p.eval(x) + q.eval(x),
            Mul(p, q) => p.eval(x) * q.eval(x),
            Sin(p) => p.eval(x).sin(),
            Cos(p) => p.eval(x).cos(),
        }
    }

    pub fn derive(&self) -> F {
        match self {
            Num(_) => Num(0.0),
            X => Num(1.0),
            Add(p, q) => Add(b(p.derive()), b(q.derive())),
            // product rule: (pq)' = p'q + pq'
            Mul(p, q) => Add(b(Mul(b(p.derive()), q.clone())),
                b(Mul(p.clone(), b(q.derive())))),
            // chain rule: (sin p)' = cos(p) p', (cos p)' = -sin(p) p'
            Sin(p) => Mul(b(Cos(p.clone())), b(p.derive())),
            Cos(p) => Mul(b(Mul(b(Num(-1.0)), b(Sin(p.clone())))), b(p.derive())),
        }
    }

    pub fn simplify(self) -> F {
        match self {
            Add(p, q) => match (p.simplify(), q.simplify()) {
                (Num(m), Num(n)) => Num(m + n),
                (Num(z), e) | (e, Num(z)) if z == 0.0 => e,
                (p, q) => Add(b(p), b(q)),
            },
            Mul(p, q) => match (p.simplify(), q.simplify()) {
                (Num(m), Num(n)) => Num(m * n),
                (Num(z), _) | (_, Num(z)) if z == 0.0 => Num(0.0),
                (Num(o), e) | (e, Num(o)) if o == 1.0 => e,
                (p, q) => Mul(b(p), b(q)),
            },
            Sin(p) => Sin(b(p.simplify())),
            Cos(p) => Cos(b(p.simplify())),
            leaf => leaf,
        }
    }

    pub fn size(&self) -> usize {
        match self {
            Num(_) | X => 1,
            Add(p, q) | Mul(p, q) => 1 + p.size() + q.size(),
            Sin(p) | Cos(p) => 1 + p.size(),
        }
    }
}
