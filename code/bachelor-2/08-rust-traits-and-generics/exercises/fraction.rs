// fraction.rs: a fraction kept in lowest terms, printed with Display (exercise 3).
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Fraction {
    num: i64,
    den: i64, // always > 0, and gcd(|num|, den) = 1
}

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a.abs()
}

impl Fraction {
    pub fn new(num: i64, den: i64) -> Option<Fraction> {
        if den == 0 {
            return None;
        }
        let g = gcd(num, den);
        let s = if den < 0 { -1 } else { 1 }; // the sign goes to the numerator
        Some(Fraction { num: s * num / g, den: s * den / g })
    }
}

impl fmt::Display for Fraction {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let text = match self.den {
            1 => format!("{}", self.num),
            d => format!("{}/{}", self.num, d),
        };
        f.pad(&text) // pad, unlike write!, honours a width such as {:>8}
    }
}
