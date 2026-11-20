// pda_demo.rs: a pushdown automaton for a^n b^n, and the automaton of a bracket grammar.
#[allow(dead_code)]
mod grammar;
#[allow(dead_code)]
mod pda;
use pda::{Move, Pda};

fn main() {
    let mv = |from, read, pop, to, push: &str| Move { from, read, pop, to,
                                                     push: push.chars().collect() };
    let anbn = Pda { start: 0, bottom: 'Z', accept: vec![2], moves: vec![
        mv(0, Some('a'), 'Z', 0, "AZ"), mv(0, Some('a'), 'A', 0, "AA"), // push an A per a
        mv(0, None, 'Z', 1, "Z"), mv(0, None, 'A', 1, "A"),           // guess the middle
        mv(1, Some('b'), 'A', 1, ""),                                  // pop an A per b
        mv(1, None, 'Z', 2, "Z"),                                      // all popped: accept
    ] };
    for w in ["", "ab", "aabb", "aab", "abab", "aaabbb"] {
        let (ok, visited) = anbn.accepts(w, 20);
        println!("a^n b^n  {:9} {ok:5}  ({visited} configurations)", format!("{w:?}"));
    }
    let brackets = Pda::from_grammar(&grammar::Grammar::parse("S -> ( S ) S | ε"));
    println!("the grammar's automaton has {} moves", brackets.moves.len());
    for w in ["()", "(()())", "())(", "((("] {
        let (ok, visited) = brackets.accepts(w, 2 * w.len() + 4);
        println!("brackets {:9} {ok:5}  ({visited} configurations)", format!("{w:?}"));
    }
}
