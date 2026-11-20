// The weekend problem's numbers.
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "../listings/lr0.rs"]
mod lr0;
#[path = "../listings/slr.rs"]
mod slr;
#[path = "../listings/lr1.rs"]
mod lr1;
#[path = "../exercises/pb_if.rs"]
mod pb;
use slr::Action;

fn load(p: &str) -> grammar::Grammar {
    lr0::augment(&grammar::Grammar::parse(&std::fs::read_to_string(p).unwrap()))
}
fn set(s: &grammar::Set) -> String {
    s.iter().cloned().collect::<Vec<_>>().join(" ")
}

#[test]
fn part_1_and_2_the_dangling_else() {
    let g = load("../listings/ifelse.grammar");
    let a = lr0::automaton(&g);
    assert_eq!(a.states.len(), 9);
    assert_eq!(set(&grammar::compute(&g).follow["S"]), "$ else");
    let t = slr::table(&g, &a);
    let c = slr::conflicts(&t);
    assert_eq!(c.len(), 1);
    assert_eq!(*c[0].0, (6, "else".to_string()));
    assert_eq!(*c[0].1, vec![Action::Shift(7), Action::Reduce(1)]);
    // the driver takes the shift: the else goes to the inner if
    let inp = ["if", "c", "then", "if", "c", "then", "other", "else", "other", "$"];
    let r = slr::parse(&g, &t, &inp, false).unwrap();
    assert_eq!(pb::if_tree(&g, &r), "if(if(o else o))");
    // taking the reduce instead rejects the same input
    let mut tr = slr::table(&g, &a);
    tr.action.get_mut(&(6, "else".to_string())).unwrap().remove(0);
    assert!(slr::parse(&g, &tr, &inp, false).is_err());
    assert!(slr::parse(&g, &tr, &["if", "c", "then", "other", "else", "other", "$"], false).is_err());
    let one = lr1::automaton1(&g);
    assert_eq!((one.states.len(), lr1::conflicts1(&g, &one)), (16, 1));
    // the matched/unmatched grammar has no conflict
    let mu = load("../exercises/ifelse_mu.grammar");
    let am = lr0::automaton(&mu);
    assert!(slr::conflicts(&slr::table(&mu, &am)).is_empty());
    assert_eq!(am.states.len(), 13);
}

#[test]
fn part_3_and_4_the_assignment_grammar() {
    let g = load("../listings/lr.grammar");
    let a = lr0::automaton(&g);
    assert_eq!(a.states.len(), 10);
    assert_eq!(set(&grammar::compute(&g).follow["R"]), "$ =");
    let t = slr::table(&g, &a);
    let c = slr::conflicts(&t);
    assert_eq!(c.len(), 1);
    assert_eq!(*c[0].0, (2, "=".to_string()));
    assert_eq!(*c[0].1, vec![Action::Shift(6), Action::Reduce(5)]);
    let one = lr1::automaton1(&g);
    assert_eq!(one.states.len(), 14);
    assert_eq!(one.states[0].len(), 8);
    assert_eq!(lr1::conflicts1(&g, &one), 0);
    assert_eq!(pb::merged(&one), vec![vec![1, 9], vec![5, 12], vec![6, 10], vec![7, 13]]);
    let la = lr1::lalr(&one);
    assert_eq!((la.states.len(), lr1::conflicts1(&g, &la)), (10, 0));
    let e = load("../listings/expr.grammar");
    let one = lr1::automaton1(&e);
    assert_eq!((one.states.len(), lr1::lalr(&one).states.len()), (22, 12));
}
