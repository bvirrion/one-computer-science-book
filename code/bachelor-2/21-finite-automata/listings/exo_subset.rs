// exo_subset.rs: the subset construction for "ends with ab" (exercise 5).
#[allow(dead_code)]
mod automaton;
use automaton::Nfa;

fn main() {
    let nfa = Nfa { alphabet: vec!['a', 'b'], start: vec![0],
                    accept: vec![false, false, true],
                    delta: vec![vec![vec![0, 1], vec![0]], vec![vec![], vec![2]],
                                vec![vec![], vec![]]],
                    eps: vec![vec![]; 3] };
    let (dfa, subsets) = nfa.determinise();
    for (i, s) in subsets.iter().enumerate() {
        let [a, b] = [0, 1].map(|x| dfa.delta[i][x].unwrap());
        let mark = if dfa.accept[i] { ", accepting" } else { "" };
        println!("{i}: {s:?}  a -> {a}, b -> {b}{mark}");
    }
}
