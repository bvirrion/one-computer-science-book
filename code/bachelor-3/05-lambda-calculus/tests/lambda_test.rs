// Tests for chapter 5: terms, reduction, Church encodings, the semantics.
#![allow(dead_code)]
#[path = "../listings/term.rs"]
mod term;
#[path = "../listings/reduce.rs"]
mod reduce;
#[path = "../listings/encode.rs"]
mod encode;
#[path = "../listings/lam.rs"]
mod lam;
#[path = "../listings/smallstep.rs"]
mod smallstep;
#[path = "../listings/bigstep.rs"]
mod bigstep;
#[path = "../exercises/ex5_noshift.rs"]
mod ex5;
#[path = "../exercises/ex6_church.rs"]
mod ex6;
#[path = "../exercises/ex12_krivine.rs"]
mod ex12;

use reduce::Strategy::*;
use term::{parse, show, Term, Term::*};

fn p(s: &str) -> Term {
    parse(s).unwrap()
}

#[test]
fn parse_and_print_round_trip() {
    for s in [r"\x. \y. x y", r"(\x. x) y", r"\f. \x. f (f x)", r"x (\y. y) z"] {
        assert_eq!(show(&p(s)), s);
    }
    assert!(matches!(p(r"\x. \y. x"), Lam(_, b) if matches!(*b, Lam(_, ref c) if matches!(**c, Var(1)))));
}

#[test]
fn exercise_1_free_variables() {
    let fv = |s: &str| term::free_vars(&p(s)).into_iter().collect::<Vec<_>>().join(",");
    assert_eq!(fv(r"\x. x y"), "y");
    assert_eq!(fv(r"(\x. x) x"), "x");
    assert_eq!(fv(r"\x. \y. z (x y) w"), "w,z");
}

#[test]
fn exercise_2_alpha_equivalence() {
    let eq = |a: &str, b: &str| term::alpha_eq(&p(a), &p(b));
    assert!(eq(r"\x. \y. x y", r"\y. \x. y x"));
    assert!(!eq(r"\x. \y. x y", r"\x. \y. y x"));
    assert!(!eq(r"\x. x z", r"\z. z z"));
}

#[test]
fn exercise_3_capture_avoided() {
    let t = p(r"(\x. \y. x y) y");
    let (nf, n, _) = reduce::run(&t, Normal, 10);
    assert_eq!((show(&nf).as_str(), n), (r"\y'. y y'", 1));
}

#[test]
fn exercise_4_predict_church_lines() {
    let line = |s: &str| {
        let t = encode::church(s);
        let (nf, a, _) = reduce::run(&t, Normal, 10_000);
        let (_, b, _) = reduce::run(&t, Applicative, 10_000);
        (a, b, encode::value(&nf))
    };
    assert_eq!(line("succ c4"), (3, 3, Some(5)));
    assert_eq!(line("plus c4 c0"), (6, 6, Some(4)));
}

#[test]
fn exercise_5_shifting_matters() {
    // \a. (\x. \y. x) a : the correct result is \a. \y. a (K applied to a).
    let body = match p(r"\x. \y. x") { Lam(_, b) => *b, _ => unreachable!() };
    let good = reduce::beta(&body, &Var(0));
    let bad = ex5::beta_noshift(&body, &Var(0));
    assert_eq!(show(&lam_a(good)), r"\a. \y. a");
    assert_eq!(show(&lam_a(bad)), r"\a. \y. y");
    let t = p(r"\a. (\x. \y. x) a");
    assert_eq!(show(&reduce::run(&t, Normal, 10).0), r"\a. \y. a");
}

fn lam_a(b: Term) -> Term {
    term::lam("a", b)
}

#[test]
fn exercise_6_is_zero_and_eq() {
    let d = encode::defs();
    let is_zero = term::parse_with(ex6::IS_ZERO, &d).unwrap();
    let eq = term::parse_with(&ex6::eq_src(), &d).unwrap();
    let (tt, ff) = (p(r"\a b. a"), p(r"\a b. b"));
    for m in 0..6 {
        let z = reduce::run(&term::app(is_zero.clone(), encode::numeral(m)), Normal, 10_000).0;
        assert!(term::alpha_eq(&z, if m == 0 { &tt } else { &ff }));
        for n in 0..6 {
            let t = term::app(term::app(eq.clone(), encode::numeral(m)), encode::numeral(n));
            let (r, _, done) = reduce::run(&t, Normal, 100_000);
            assert!(done && term::alpha_eq(&r, if m == n { &tt } else { &ff }), "{m} {n}");
        }
    }
}

#[test]
fn exercise_7_call_by_name_stops_early() {
    let t = encode::church("plus c2 c3");
    let (w, _, done) = reduce::run(&t, ByName, 100);
    assert!(done);
    let n = encode::numeral(5);
    assert!(!term::alpha_eq(&w, &n));
    assert_eq!(show(&w), r"\f. \x. (\f'. \x'. f' (f' x')) f ((\f'. \x'. f' (f' (f' x'))) f x)");
    assert!(term::alpha_eq(&reduce::run(&w, Normal, 100).0, &n));
}

#[test]
fn exercise_8_mult_steps() {
    for m in 0..7 {
        for n in 0..7 {
            let t = encode::church(&format!("mult c{m} c{n}"));
            let (nf, k, _) = reduce::run(&t, Normal, 10_000);
            assert_eq!(k, 2 * m + 3);
            assert_eq!(encode::value(&nf), Some(m * n));
        }
    }
}

#[test]
fn exercise_11_omega() {
    let omega = r"(\x. x x) (\x. x x)";
    let w = p(omega);
    assert!(term::alpha_eq(&reduce::step(&w, Normal).unwrap(), &w)); // Ω -> Ω, its only redex
    let kio = p(&format!(r"(\x. \y. x) (\z. z) ({omega})"));
    let (r, k, done) = reduce::run(&kio, Normal, 100);
    assert!(done && k == 2 && show(&r) == r"\z. z");
    let (_, _, done) = reduce::run(&kio, ByValue, 1000);
    assert!(!done);
}

#[test]
fn exercise_12_krivine_matches_call_by_name() {
    let mut terms: Vec<Term> = ["succ c2", "plus c2 c3", "mult c3 c2", "pred c4", "exp c2 c3", "fst (pair c1 c2)"]
        .iter().map(|s| encode::church(s)).collect();
    terms.push(p(r"(\x. \y. x) (\z. z) ((\x. x x) (\x. x x))"));
    terms.push(p(r"(\x. x a) (\y. y)"));
    for t in terms {
        let (w, k, done) = reduce::run(&t, ByName, 10_000);
        assert!(done);
        let (w2, k2) = ex12::krivine(&t, 100_000).unwrap();
        assert!(term::alpha_eq(&w, &w2), "{} vs {}", show(&w), show(&w2));
        assert_eq!(k, k2);
    }
}

/// Every term one β-step away (any redex, anywhere).
fn all_steps(t: &Term) -> Vec<Term> {
    let mut out = vec![];
    match t {
        Var(_) | Free(_) => {}
        Lam(x, b) => out.extend(all_steps(b).into_iter().map(|b| Lam(x.clone(), Box::new(b)))),
        App(f, a) => {
            if let Lam(_, b) = &**f {
                out.push(reduce::beta(b, a));
            }
            out.extend(all_steps(f).into_iter().map(|f| App(Box::new(f), a.clone())));
            out.extend(all_steps(a).into_iter().map(|a| App(f.clone(), Box::new(a))));
        }
    }
    out
}

#[test]
fn reduction_graph_of_the_figure() {
    let t = p(r"(\x. x x) ((\y. y) a)");
    let mut seen: Vec<String> = vec![show(&t)];
    let mut edges = vec![];
    let mut todo = vec![t];
    while let Some(u) = todo.pop() {
        for v in all_steps(&u) {
            edges.push((show(&u), show(&v)));
            if !seen.contains(&show(&v)) {
                seen.push(show(&v));
                todo.push(v);
            }
        }
    }
    seen.sort();
    assert_eq!(seen, [r"(\x. x x) ((\y. y) a)", r"(\x. x x) a", r"(\y. y) a ((\y. y) a)", r"(\y. y) a a", "a ((\\y. y) a)", "a a"]);
    assert_eq!(edges.len(), 7);
    let path = |s| reduce::run(&p(r"(\x. x x) ((\y. y) a)"), s, 10).1;
    assert_eq!((path(Normal), path(ByValue), path(Applicative), path(ByName)), (3, 2, 2, 2));
}

#[test]
fn strategies_on_church_terms() {
    let t = encode::church("pred c3");
    assert_eq!(reduce::run(&t, Normal, 1000).1, 36);
    assert_eq!(reduce::run(&t, Applicative, 1000).1, 43);
}

fn lam_run(src: &str) -> (Result<lam::E, String>, usize) {
    smallstep::run(&lam::parse(src).unwrap(), 100_000, &mut |_, _| {})
}

#[test]
fn small_and_big_step_agree() {
    let progs = [
        include_str!("../listings/sum.lam").to_string(),
        "let x = 3 in let y = x * x in (y, y < 10)".into(),
        r"letrec fact = \n. if n == 0 then 1 else n * fact (n - 1) in fact 6".into(),
        r"(\p. snd p + fst p) (1 + 1, 40)".into(),
        r"let twice = \f. \x. f (f x) in twice (twice (\k. k + 3)) 0".into(),
        r"if 1 < 2 then (\x. x) else (\x. 0)".into(),
    ];
    for src in progs {
        let e = lam::parse(&src).unwrap();
        let (v, steps) = lam_run(&src);
        let mut z = bigstep::Size::default();
        let w = bigstep::eval(&e, &mut z, 0).unwrap();
        assert_eq!(v.unwrap(), w, "{src}");
        assert_eq!(steps, z.contractions, "{src}");
    }
    let e = lam::parse(r"(\x. x + 1) 2").unwrap();
    let mut z = bigstep::Size::default();
    bigstep::eval(&e, &mut z, 0).unwrap();
    assert_eq!((z.nodes, z.contractions, lam_run(r"(\x. x + 1) 2").1), (6, 2, 2));
    let (v, n) = lam_run(include_str!("../listings/sum.lam"));
    assert_eq!((lam::show(&v.unwrap()), n), ("6".to_string(), 23));
}

#[test]
fn stuck_terms_and_errors() {
    assert!(lam_run("1 2").0.unwrap_err().contains("not a function"));
    assert!(lam_run("if 3 then 1 else 2").0.unwrap_err().contains("not a boolean"));
    assert!(lam_run("fst 3").0.unwrap_err().contains("not a pair"));
    assert!(lam_run("true + 1").0.unwrap_err().contains("cannot apply"));
    assert!(lam::parse("letrec f = 3 in f").is_err());
}

#[test]
fn lam_printer_round_trips() {
    for s in [r"\x. x + 1", "let x = 1 in x * (x + 2)", r"(\x. x) 3", "if a < b then (a, b) else fst c",
              r"\x: int -> bool. x 1", r"\p: int * bool. snd p", "f (g x) (h y)", "1 - (2 - 3)",
              r"\f: (int -> int) -> int. f (\y. y)"] {
        let e = lam::parse(s).unwrap();
        assert_eq!(lam::show(&e), s);
        assert_eq!(lam::parse(&lam::show(&e)).unwrap(), e);
    }
}
