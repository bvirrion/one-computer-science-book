// Tests for chapter 6: the checker, unification, inference, safety.
#![allow(dead_code)]
#[path = "../../05-lambda-calculus/listings/lam.rs"]
mod lam;
#[path = "../../05-lambda-calculus/listings/smallstep.rs"]
mod smallstep;
#[path = "../listings/check.rs"]
mod check;
#[path = "../listings/unify.rs"]
mod unify;
#[path = "../listings/infer.rs"]
mod infer;
#[path = "../exercises/ex5_noocc.rs"]
mod ex5;
#[path = "../exercises/ex6_pairs.rs"]
mod ex6;

use lam::{parse, show_ty, Ty};

fn checked(src: &str) -> Result<String, String> {
    check::derive(&vec![], &parse(src).unwrap()).map(|d| show_ty(&d.ty))
}
fn inferred(src: &str) -> Result<String, String> {
    infer::principal(&parse(src).unwrap()).map(|t| show_ty(&t))
}
fn v(k: u32) -> Ty {
    Ty::Var(k)
}
fn fun(a: Ty, b: Ty) -> Ty {
    Ty::Fun(Box::new(a), Box::new(b))
}
fn pair(a: Ty, b: Ty) -> Ty {
    Ty::Pair(Box::new(a), Box::new(b))
}

#[test]
fn the_demo_derivation() {
    let e = parse(r"(\f: int -> int. f (f 3)) (\x: int. x * 2)").unwrap();
    let d = check::derive(&vec![], &e).unwrap();
    let mut lines = vec![];
    check::print(&d, 0, &mut lines);
    assert_eq!((show_ty(&d.ty), lines.len()), ("int".to_string(), 11));
}

#[test]
fn exercise_1_types_of_terms() {
    assert_eq!(checked(r"\x: int. \y: bool. if y then x else 0").unwrap(), "int -> bool -> int");
    assert_eq!(checked(r"\f: int -> int. \x: int. f (f x)").unwrap(), "(int -> int) -> int -> int");
    assert_eq!(checked(r"(\x: bool. x) true").unwrap(), "bool");
}

#[test]
fn exercise_2_derivation() {
    let d = check::derive(&vec![], &parse(r"\x: int. \f: int -> bool. f x").unwrap()).unwrap();
    let mut lines = vec![];
    check::print(&d, 0, &mut lines);
    assert_eq!(show_ty(&d.ty), "int -> (int -> bool) -> bool");
    assert_eq!(lines.len(), 5);
    assert_eq!(lines[2].trim(), "x: int, f: int -> bool |- f x : bool   [app]");
}

#[test]
fn exercise_3_typable_or_not() {
    assert!(inferred(r"\x. x x").is_err());
    assert_eq!(inferred(r"\f. \x. f x x").unwrap(), "('a -> 'a -> 'b) -> 'a -> 'b");
    assert_eq!(inferred(r"\p. fst p + snd p").unwrap(), "int * int -> int");
    assert!(inferred(r"\x. if x then x else 1").is_err());
}

#[test]
fn exercise_4_twice() {
    assert_eq!(inferred(r"\f. \x. f (f x)").unwrap(), "('a -> 'a) -> 'a -> 'a");
}

#[test]
fn exercise_5_occurs_check() {
    // \x. x x : x has type a; the application asks a = a -> b.
    let eq = fun(v(0), v(1));
    let mut s = ex5::Tri::new();
    ex5::unify(&mut s, &v(0), &eq, false).unwrap(); // accepted: a := a -> b
    let mut fuel = 1_000;
    assert!(ex5::resolve(&s, &v(0), &mut fuel).is_none()); // printing a never ends
    let mut s = ex5::Tri::new();
    assert!(ex5::unify(&mut s, &v(0), &eq, true).is_err());
}

#[test]
fn exercise_6_pairs() {
    let t = |s: &str| ex6::type_of(&[], &parse(s).unwrap()).map(|t| show_ty(&t));
    assert_eq!(t(r"(\p: int * bool. if snd p then fst p else 0) (1, true)").unwrap(), "int");
    assert_eq!(t(r"\p: int * (int -> bool). snd p (fst p)").unwrap(), "int * (int -> bool) -> bool");
    assert!(t("fst 3").is_err());
    assert_eq!(t(r"(\x: int. x + 1) 2").unwrap(), "int");
}

#[test]
fn exercise_9_self_application() {
    assert_eq!(inferred(r"let id = \x. x in id id").unwrap(), "'a -> 'a");
    assert!(inferred(r"(\id. id id) (\x. x)").is_err());
}

#[test]
fn exercise_11_let_polymorphism_is_needed() {
    let e = parse(r"let id = \x. x in (id 1, id true)").unwrap();
    let mut quiet = |_: &str, _: &infer::Scheme| {};
    let mut mono = infer::Infer::new(&mut quiet);
    mono.generalise = false;
    assert!(mono.infer(&vec![], &e).is_err());
    assert_eq!(inferred(r"let id = \x. x in (id 1, id true)").unwrap(), "int * bool");
}

#[test]
fn unification_of_the_figure() {
    let mut s = unify::Subst::new();
    let t1 = pair(fun(v(0), v(1)), v(0));
    let t2 = pair(fun(Ty::Int, Ty::Bool), v(2));
    unify::unify(&mut s, &t1, &t2).unwrap();
    let got: Vec<String> = s.iter().map(|(k, t)| format!("{}:={}", show_ty(&v(*k)), show_ty(t))).collect();
    assert_eq!(got, ["'a:=int", "'b:=bool", "'c:=int"]);
    assert_eq!(unify::apply(&s, &t1), unify::apply(&s, &t2));
    // a mismatch, and the occurs check
    assert!(unify::unify(&mut unify::Subst::new(), &fun(v(0), Ty::Int), &pair(v(1), v(2))).is_err());
    assert!(unify::unify(&mut unify::Subst::new(), &v(0), &pair(v(0), Ty::Int)).is_err());
}

#[test]
fn most_general_unifiers_are_most_general() {
    // 'a -> 'b against 'c -> int: the mgu keeps 'a free (as 'c or 'a).
    let mut s = unify::Subst::new();
    unify::unify(&mut s, &fun(v(0), v(1)), &fun(v(2), Ty::Int)).unwrap();
    let t = unify::apply(&s, &fun(v(0), v(1)));
    assert_eq!(show_ty(&unify::normalise(&t)), "'a -> int");
}

#[test]
fn poly_lam_types() {
    let src = include_str!("../listings/poly.lam");
    let mut seen = vec![];
    let mut rec = |name: &str, sc: &infer::Scheme| {
        seen.push(format!("{name} {} {}", sc.vars.len(), show_ty(&unify::normalise(&sc.ty))));
    };
    let mut inf = infer::Infer::new(&mut rec);
    let t = inf.infer(&vec![], &parse(src).unwrap()).unwrap();
    drop(inf);
    assert_eq!(show_ty(&t), "int * bool");
    assert_eq!(seen[3], "swap 2 'a * 'b -> 'b * 'a");
    assert_eq!(seen[4], "count 0 int -> int");
}

#[test]
fn checker_rejections() {
    assert!(checked(r"\x. x").unwrap_err().contains("no type"));
    assert!(checked(r"(\x: int. x) true").unwrap_err().contains("expects int, not bool"));
    assert!(checked(r"3 4").unwrap_err().contains("not a function"));
    assert!(checked("if 1 then 2 else 3").unwrap_err().contains("not a bool"));
}

/// Progress and preservation, checked along whole runs.
#[test]
fn safety_on_sample_programs() {
    let progs = [
        include_str!("../../05-lambda-calculus/listings/sum.lam"),
        include_str!("../listings/poly.lam"),
        r"let twice = \f. \x. f (f x) in (twice (\k. k * 3) 1, twice (\b. if b then false else true) true)",
        r"letrec fact = \n. if n < 1 then 1 else n * fact (n - 1) in fact 5 == 120",
        r"let p = (1, (2, 3)) in fst (snd p) + snd (snd p)",
    ];
    for src in progs {
        let mut e = parse(src).unwrap();
        let t = infer::principal(&e).unwrap();
        let mut steps = 0;
        while !smallstep::is_value(&e) {
            e = smallstep::step(&e).expect("progress: a well-typed term is not stuck");
            assert_eq!(infer::principal(&e).unwrap(), t, "preservation after step {steps} of {src}");
            steps += 1;
        }
        assert!(steps > 0);
    }
}
