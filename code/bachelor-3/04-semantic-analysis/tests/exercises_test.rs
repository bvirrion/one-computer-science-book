// Tests of the exercise solutions.
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "../../02-top-down-parsing/listings/ast.rs"]
mod ast;
#[path = "../../02-top-down-parsing/listings/parser.rs"]
mod parser;
#[path = "../listings/scope.rs"]
mod scope;
#[path = "../listings/resolve.rs"]
mod resolve;
#[path = "../listings/typecheck.rs"]
mod typecheck;
#[path = "../listings/interp.rs"]
mod interp;
#[path = "../exercises/ex5_flat_fixed.rs"]
mod ex5;
#[path = "../exercises/ex6_unused.rs"]
mod ex6;
#[path = "../exercises/ex11_persistent.rs"]
mod ex11;

#[test]
fn exercise_5_restores_the_outer_declaration() {
    let mut s = ex5::Flat::new();
    s.enter();
    s.declare("x", 15);
    s.enter();
    s.declare("x", 17);
    assert_eq!(s.lookup("x"), Some(17));
    s.exit();
    assert_eq!(s.lookup("x"), Some(15));
    s.exit();
    assert_eq!(s.lookup("x"), None);
}

#[test]
fn exercise_6_unused_variables() {
    let src = std::fs::read_to_string("../exercises/ex6.moor").unwrap();
    let p = parser::parse_source(&src, "ex6.moor").unwrap();
    let r = resolve::resolve(&p);
    let w: Vec<(String, u32)> = ex6::unused(&p, &r).iter().map(|d| (d.msg.clone(), d.span.line)).collect();
    assert_eq!(w, vec![("'unit' is never read".to_string(), 1), ("'spare' is never read".to_string(), 3),
                       ("'total' is never read".to_string(), 10)]);
}

#[test]
fn exercise_8_probes_grow_with_depth() {
    // a use at depth k of a name declared at depth 1 probes k maps
    for d in 1..=20usize {
        let mut s: scope::Scopes<u32> = scope::Scopes::new();
        s.declare("g", 0).unwrap();
        for _ in 1..d {
            s.push();
        }
        s.lookup("g");
        assert_eq!(s.probes, d as u64);
        s.lookup("nowhere");
        assert_eq!(s.probes, 2 * d as u64);
    }
}

#[test]
fn exercise_11_persistent_scopes() {
    let mut c = ex11::Counts::default();
    let mut outer = None;
    for k in 0..1000u32 {
        outer = ex11::insert(&outer, &format!("v{k}"), k, &mut c);
    }
    assert!(ex11::height(&outer) <= 14); // 1.44 log2(1001) < 14.4
    let n_outer = c.nodes;
    assert!(n_outer < 1000 * 16);
    // an inner block shadows v7 and adds w; the outer tree is untouched
    let mut inner = ex11::insert(&outer, "v7", 700, &mut c);
    inner = ex11::insert(&inner, "w", 1, &mut c);
    assert!(c.nodes - n_outer <= 2 * 3 * 14);
    assert_eq!(ex11::lookup(&inner, "v7", &mut c), Some(700));
    assert_eq!(ex11::lookup(&outer, "v7", &mut c), Some(7));
    assert_eq!(ex11::lookup(&outer, "w", &mut c), None);
    let before = c.comparisons;
    ex11::lookup(&outer, "v999", &mut c);
    assert!(c.comparisons - before <= 14);
}
