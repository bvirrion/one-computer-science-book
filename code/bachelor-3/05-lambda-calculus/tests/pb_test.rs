// The weekend problem's counts: β-steps of Church arithmetic, fitted.
#![allow(dead_code)]
#[path = "../listings/term.rs"]
mod term;
#[path = "../listings/reduce.rs"]
mod reduce;
#[path = "../listings/encode.rs"]
mod encode;
use reduce::Strategy::{self, Applicative, Normal};

fn steps(src: &str, s: Strategy) -> (usize, Option<usize>) {
    let (nf, k, done) = reduce::run(&encode::church(src), s, 1_000_000);
    assert!(done);
    (k, encode::value(&nf))
}

#[test]
fn addition_and_multiplication() {
    for m in 0..=9 {
        for n in 0..=9 {
            if m + n <= 9 {
                assert_eq!(steps(&format!("plus c{m} c{n}"), Normal), (6, Some(m + n)));
            }
            assert_eq!(steps(&format!("mult c{m} c{n}"), Applicative).0, 2 * m + 3);
        }
    }
}

#[test]
fn exponentiation_doubles_under_normal_order() {
    for n in 1..=6 {
        let (k, v) = steps(&format!("exp c2 c{n}"), Normal);
        assert_eq!((k, v), (1 << (n + 1), Some(1 << n)));
        assert_eq!(steps(&format!("exp c2 c{n}"), Applicative).0, 3 * n + 1);
    }
}

#[test]
fn predecessor_is_linear() {
    assert_eq!(steps("pred c0", Normal), (9, Some(0)));
    for n in 1..=9 {
        assert_eq!(steps(&format!("pred c{n}"), Normal), (10 * n + 6, Some(n - 1)));
        let app = steps(&format!("pred c{n}"), Applicative).0;
        assert_eq!(app, if n == 1 { 23 } else { 9 * n + 16 });
    }
}

#[test]
fn subtraction_is_quadratic() {
    let d = encode::defs();
    let sub = term::parse_with(r"\m n. n pred m", &d).unwrap();
    for m in 0..=12 {
        for n in 0..=m {
            let t = term::app(term::app(sub.clone(), encode::numeral(m)), encode::numeral(n));
            let (nf, k, _) = reduce::run(&t, Normal, 1_000_000);
            assert_eq!(encode::value(&nf), Some(m - n));
            assert_eq!(k as i64, 10 * (m * n) as i64 - 5 * (n * n) as i64 + 11 * n as i64 + 4, "{m} {n}");
        }
    }
}

#[test]
fn addition_by_successor() {
    let d = encode::defs();
    let add = term::parse_with(r"\m n. m succ n", &d).unwrap();
    for m in 0..=6 {
        for n in 0..=3 {
            let t = term::app(term::app(add.clone(), encode::numeral(m)), encode::numeral(n));
            let (nf, k, _) = reduce::run(&t, Normal, 100_000);
            assert_eq!((encode::value(&nf), k), (Some(m + n), 3 * m + 4), "{m} {n}");
        }
    }
}
