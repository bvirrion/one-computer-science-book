// Tests of the grammar tools (listings/grammar.rs) and the grammar files.
#[path = "../listings/grammar.rs"]
mod grammar;
use grammar::{compute, table, Grammar};

fn load(path: &str) -> Grammar {
    Grammar::parse(&std::fs::read_to_string(path).unwrap())
}
fn set(s: &grammar::Set) -> String {
    s.iter().cloned().collect::<Vec<_>>().join(" ")
}
fn conflicts(g: &Grammar) -> usize {
    table(g, &compute(g)).values().filter(|r| r.len() > 1).count()
}

#[test]
fn expr_grammar_sets() {
    let g = load("../listings/expr.grammar");
    let s = compute(&g);
    assert_eq!(set(&s.first["E"]), "( id");
    assert_eq!(set(&s.follow["T"]), "$ ) +");
    assert_eq!(set(&s.follow["F"]), "$ ) * +");
    assert_eq!(s.nullable.len(), 2);
    assert_eq!(conflicts(&g), 0);
}

#[test]
fn left_factoring_removes_the_conflict() {
    assert_eq!(conflicts(&load("../listings/stmt.grammar")), 1);
    assert_eq!(conflicts(&load("../listings/stmt_factored.grammar")), 0);
}

#[test]
fn moor_is_ll1() {
    let g = load("../listings/moor.grammar");
    assert_eq!(g.nonterms.len(), 37);
    assert_eq!(conflicts(&g), 0);
}

#[test]
fn exercise_grammars() {
    let g = load("../exercises/ex1.grammar");
    let s = compute(&g);
    assert_eq!((set(&s.first["S"]), set(&s.first["A"]), set(&s.first["B"])), ("a b c d".into(), "a".into(), "b".into()));
    let g3 = load("../exercises/ex3.grammar");
    let t = table(&g3, &compute(&g3));
    assert_eq!(t[&("A".to_string(), "a".to_string())].len(), 2);
    assert_eq!(conflicts(&load("../exercises/ex6_moor_for.grammar")), 0);
}

#[test]
fn a_left_recursive_rule_always_conflicts() {
    let g = Grammar::parse("L -> L , id | id");
    assert_eq!(conflicts(&g), 1);
    let fixed = Grammar::parse("L -> id L'\nL' -> , id L' | eps");
    assert_eq!(conflicts(&fixed), 0);
}

#[test]
fn fines_grammars_are_ll1() {
    let g = load("../exercises/fines.grammar");
    assert_eq!(g.nonterms.len(), 17);
    assert_eq!(conflicts(&g), 0);
    let s = compute(&g);
    assert_eq!(set(&s.first["E"]), "( name num");
    assert_eq!(set(&s.follow["U"]), "!= $ ) * + , - / < <= == > >= ^ and or");
    assert_eq!(set(&s.follow["S'"]), "!= $ ) , < <= == > >= and or");
    let t = table(&g, &s);
    let eps_cols: Vec<&str> = t.iter().filter(|((a, _), r)| a == "S'" && g.rules[r[0]].1.is_empty()).map(|((_, x), _)| x.as_str()).collect();
    assert_eq!(eps_cols.len(), 11);
    assert_eq!(conflicts(&load("../exercises/fines_neg.grammar")), 0);
}
