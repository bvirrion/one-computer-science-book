// exo_closure_bug.rs: a closure that takes one spontaneous step only (exercise 6).
#[allow(dead_code)]
mod automaton;
use automaton::{Nfa, Subset};

fn one_step(n: &Nfa, set: &Subset) -> Subset {
    let mut out = set.clone();
    for &q in set {
        out.extend(n.eps[q].iter().copied()); // the bug: no loop on the new states
    }
    out
}

fn main() {
    let n = Nfa { // a*b*c* of epsilon.rs
        alphabet: vec!['a', 'b', 'c'], start: vec![0], accept: vec![false, false, true],
        delta: vec![vec![vec![0], vec![], vec![]], vec![vec![], vec![1], vec![]],
                    vec![vec![], vec![], vec![2]]],
        eps: vec![vec![1], vec![2], vec![]],
    };
    for w in ["", "a", "ab", "abc", "c"] {
        let mut set = one_step(&n, &Subset::from([0]));
        for c in w.chars() {
            let a = n.alphabet.iter().position(|&x| x == c).unwrap();
            let next = set.iter().flat_map(|&q| n.delta[q][a].iter().copied()).collect();
            set = one_step(&n, &next);
        }
        let wrong = set.iter().any(|&q| n.accept[q]);
        println!("{:6} one step: {:5}  closure: {}", format!("{w:?}"), wrong, n.accepts(w));
    }
}
