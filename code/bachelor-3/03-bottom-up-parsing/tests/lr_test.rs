// Tests of the LR(0) automaton, the SLR table and the driver.
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "../listings/lr0.rs"]
mod lr0;
#[path = "../listings/slr.rs"]
mod slr;
use slr::Action;

fn load(p: &str) -> grammar::Grammar {
    lr0::augment(&grammar::Grammar::parse(&std::fs::read_to_string(p).unwrap()))
}
fn words(s: &str) -> Vec<&str> {
    let mut v: Vec<&str> = s.split(' ').collect();
    v.push("$");
    v
}

#[test]
fn expression_automaton_has_twelve_states() {
    let g = load("../listings/expr.grammar");
    let a = lr0::automaton(&g);
    assert_eq!(a.states.len(), 12);
    assert_eq!(a.trans.len(), 22);
    assert_eq!(a.states[0].len(), 7);
    let t = slr::table(&g, &a);
    assert!(slr::conflicts(&t).is_empty());
    assert_eq!(t.action[&(2, "*".to_string())], vec![Action::Shift(7)]);
    assert_eq!(t.action[&(2, "+".to_string())], vec![Action::Reduce(2)]);
}

#[test]
fn exercise_1_closure() {
    let g = load("../listings/expr.grammar");
    let k = lr0::State::from([(5, 1)]); // F -> ( . E )
    assert_eq!(lr0::show_item(&g, (5, 1)), "F -> ( . E )");
    let c = lr0::closure(&g, &k);
    assert_eq!(c.len(), 7);
    assert_eq!(c, lr0::automaton(&g).states[4]);
}

#[test]
fn a_rightmost_derivation_in_reverse() {
    let g = load("../listings/expr.grammar");
    let t = slr::table(&g, &lr0::automaton(&g));
    assert_eq!(slr::parse(&g, &t, &words("id + id * id"), false).unwrap(), vec![6, 4, 2, 6, 4, 6, 3, 1]);
    // exercise 3: T * F is reduced while + id is still unread
    assert_eq!(slr::parse(&g, &t, &words("id * id + id"), false).unwrap(), vec![6, 4, 6, 3, 2, 6, 4, 1]);
    // exercise 2: ( id ) * id
    assert_eq!(slr::parse(&g, &t, &words("( id ) * id"), false).unwrap(), vec![6, 4, 2, 5, 4, 6, 3, 2]);
}

#[test]
fn exercise_9_errors() {
    let g = load("../listings/expr.grammar");
    let t = slr::table(&g, &lr0::automaton(&g));
    assert_eq!(slr::parse(&g, &t, &words("id + * id"), false), Err("unexpected * in state 6".into()));
    assert_eq!(slr::parse(&g, &t, &words("( id + id"), false), Err("unexpected $ in state 8".into()));
    assert_eq!(slr::parse(&g, &t, &words("id id"), false), Err("unexpected id in state 5".into()));
}

#[test]
fn exercise_7_parentheses() {
    let g = load("../exercises/ex7.grammar");
    let a = lr0::automaton(&g);
    assert_eq!(a.states.len(), 6);
    assert!(slr::conflicts(&slr::table(&g, &a)).is_empty());
}
