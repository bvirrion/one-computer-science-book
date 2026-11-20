// epsilon.rs: a*b*c* with spontaneous transitions, their closures, and their removal.
#[allow(dead_code)]
mod automaton;
use automaton::{Nfa, Subset};

fn words(alphabet: &[char], n: usize) -> Vec<String> {
    let mut all = vec![String::new()];
    let mut layer = vec![String::new()];
    for _ in 0..n {
        layer = layer.iter().flat_map(|w| alphabet.iter().map(move |c| format!("{w}{c}")))
            .collect();
        all.extend(layer.iter().cloned());
    }
    all
}

/// The same language without spontaneous transitions.
fn remove_eps(n: &Nfa) -> Nfa {
    let states = n.delta.len();
    let cl: Vec<Subset> = (0..states).map(|q| n.closure(&Subset::from([q]))).collect();
    let delta = (0..states)
        .map(|q| (0..n.alphabet.len()).map(|a| n.step(&cl[q], a).into_iter().collect())
            .collect())
        .collect();
    let accept = (0..states).map(|q| cl[q].iter().any(|&p| n.accept[p])).collect();
    Nfa { alphabet: n.alphabet.clone(), delta, eps: vec![vec![]; states],
          start: n.start.clone(), accept }
}

fn main() {
    let n = Nfa {
        alphabet: vec!['a', 'b', 'c'],
        delta: vec![vec![vec![0], vec![], vec![]],  // 0 loops on a
                    vec![vec![], vec![1], vec![]],  // 1 loops on b
                    vec![vec![], vec![], vec![2]]], // 2 loops on c
        eps: vec![vec![1], vec![2], vec![]], // 0 -> 1 -> 2 for free
        start: vec![0],
        accept: vec![false, false, true],
    };
    for q in 0..3 {
        println!("closure of {q}: {:?}", n.closure(&Subset::from([q])));
    }
    let m = remove_eps(&n);
    for (q, row) in m.delta.iter().enumerate() {
        println!("state {q}: a -> {:?}, b -> {:?}, c -> {:?}{}", row[0], row[1], row[2],
                 if m.accept[q] { "  accepting" } else { "" });
    }
    let all = words(&n.alphabet, 6);
    let same = all.iter().filter(|w| n.accepts(w) == m.accepts(w)).count();
    let accepted = all.iter().filter(|w| m.accepts(w)).count();
    println!("{same} of {} words up to length 6 judged alike; {accepted} accepted",
             all.len());
}
