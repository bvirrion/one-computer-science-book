// encode.rs -- Church numerals, booleans and pairs: the definitions,
// and a parser that knows them.
#![allow(dead_code)]
use crate::term::{self, Term};

/// The Church numeral n: \f. \x. f (f ... (f x)), n applications.
pub fn numeral(n: usize) -> Term {
    let mut body = Term::Var(0);
    for _ in 0..n {
        body = term::app(Term::Var(1), body);
    }
    term::lam("f", term::lam("x", body))
}

/// The value of a term in normal form that is a numeral, if it is one.
pub fn value(t: &Term) -> Option<usize> {
    (0..=256).find(|&n| term::alpha_eq(t, &numeral(n)))
}

/// Each definition may use the ones before it.
pub fn defs() -> Vec<(&'static str, Term)> {
    let src = [
        ("true", r"\a b. a"), ("false", r"\a b. b"),
        ("pair", r"\a b f. f a b"), ("fst", r"\p. p true"), ("snd", r"\p. p false"),
        ("zero", r"\f x. x"), ("succ", r"\n f x. f (n f x)"),
        ("plus", r"\m n f x. m f (n f x)"), ("mult", r"\m n f. m (n f)"),
        ("exp", r"\m n. n m"),
        ("pred", r"\n. fst (n (\p. pair (snd p) (succ (snd p))) (pair zero zero))"),
    ];
    let mut out: Vec<(&str, Term)> = vec![];
    for (name, s) in src {
        let t = term::parse_with(s, &out).expect("a definition");
        out.push((name, t));
    }
    out
}

/// Parse with the definitions and the numerals 0..9 as names c0..c9.
pub fn church(src: &str) -> Term {
    let mut d = defs();
    let names = ["c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"];
    for (k, n) in names.iter().enumerate() {
        d.push((n, numeral(k)));
    }
    term::parse_with(src, &d).expect("a term")
}
