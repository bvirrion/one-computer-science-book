// Tests of the exercise solutions.
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "../listings/lr0.rs"]
mod lr0;
#[path = "../listings/slr.rs"]
mod slr;
#[path = "../listings/lr1.rs"]
mod lr1;
#[path = "../exercises/ex6_prec.rs"]
mod ex6;
#[path = "../exercises/ex11_family.rs"]
mod ex11;
#[path = "../exercises/ex12_lalr_prop.rs"]
mod ex12;
use std::collections::BTreeSet;

fn load(p: &str) -> grammar::Grammar {
    lr0::augment(&grammar::Grammar::parse(&std::fs::read_to_string(p).unwrap()))
}

#[test]
fn exercise_5_goto_needs_the_closure() {
    // the kernel-only goto of listings/kernel_bug.rs gives 12 states too, but
    // states without closure items: the fix is lr0::goto, which closes.
    let g = load("../listings/expr.grammar");
    let a = lr0::automaton(&g);
    let kernel = lr0::State::from([(1, 2)]); // E -> E + . T
    assert_eq!(lr0::goto(&g, &a.states[1], "+"), lr0::closure(&g, &kernel));
    assert_eq!(a.states[6].len(), 5);
    let t = slr::table(&g, &a);
    assert!(slr::parse(&g, &t, &["id", "+", "id", "$"], false).is_ok());
}

#[test]
fn exercise_6_precedence() {
    use ex6::{Assoc::*, Prec};
    let g = load("../exercises/ambig.grammar");
    assert_eq!(slr::conflicts(&slr::table(&g, &lr0::automaton(&g))).len(), 25);
    let p = Prec(vec![("==", 1, Non), ("+", 2, Left), ("-", 2, Left), ("*", 3, Left), ("^", 4, Right)]);
    let t = ex6::table(&g, &p);
    assert!(slr::conflicts(&t).is_empty());
    let tree = |s: &str| {
        let mut v: Vec<&str> = s.split(' ').collect();
        v.push("$");
        ex6::tree(&g, &t, &v)
    };
    assert_eq!(tree("id + id * id").unwrap(), "(+ id (* id id))");
    assert_eq!(tree("id - id - id").unwrap(), "(- (- id id) id)");
    assert_eq!(tree("id ^ id ^ id").unwrap(), "(^ id (^ id id))");
    assert_eq!(tree("id * ( id + id ) ^ id").unwrap(), "(* id (^ (+ id id) id))");
    assert_eq!(tree("id == id + id").unwrap(), "(== id (+ id id))");
    assert!(tree("id == id == id").is_err());
}

#[test]
fn exercise_11_exponential_family() {
    for n in 1..=7usize {
        let g = lr0::augment(&grammar::Grammar::parse(&ex11::family(n)));
        assert_eq!(g.rules.len(), n * n + n + 1);
        assert_eq!(lr0::automaton(&g).states.len(), n * (1 << n) + n * n - n + 2);
    }
}

#[test]
fn exercise_12_propagation_equals_merging() {
    for f in ["../listings/expr.grammar", "../listings/ifelse.grammar", "../listings/lr.grammar",
              "../exercises/ambig.grammar", "../exercises/ifelse_mu.grammar", "../listings/moor_expr.grammar"] {
        let g = load(f);
        let merged = lr1::lalr(&lr1::automaton1(&g));
        let (a, la) = ex12::lookaheads(&g);
        assert_eq!(merged.states.len(), a.states.len(), "{f}");
        for s in &merged.states {
            let k = a.states.iter().position(|x| *x == lr1::core(s)).unwrap();
            for (it, set) in &la[k] {
                let theirs: BTreeSet<String> = s.iter().filter(|(r, d, _)| (*r, *d) == *it).map(|x| x.2.clone()).collect();
                assert_eq!(&theirs, set, "{f}");
            }
        }
    }
}
