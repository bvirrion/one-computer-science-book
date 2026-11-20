// dfa.rs: complete DFAs from expressions, Moore's minimisation, equivalence, elimination.
use crate::regex::{alt, cat, star, Glushkov, Re};
use std::collections::{BTreeSet, HashMap, VecDeque};

/// A complete DFA; the start state is 0.
pub struct Dfa {
    pub alphabet: Vec<char>,
    pub delta: Vec<Vec<usize>>,
    pub accept: Vec<bool>,
}

impl Dfa {
    pub fn accepts(&self, word: &str) -> bool {
        let mut q = 0;
        for c in word.chars() {
            match self.alphabet.iter().position(|&a| a == c) {
                Some(a) => q = self.delta[q][a],
                None => return false,
            }
        }
        self.accept[q]
    }
}

/// The subset construction on the Glushkov automaton; the empty set is the sink.
pub fn determinise(g: &Glushkov, alphabet: &[char]) -> Dfa {
    let succ = |j: usize| if j == 0 { &g.first } else { &g.follow[j] };
    let start = BTreeSet::from([0]);
    let mut index = HashMap::from([(start.clone(), 0)]);
    let (mut sets, mut delta) = (vec![start], vec![]);
    let mut todo = VecDeque::from([0]);
    while let Some(i) = todo.pop_front() {
        let mut row = vec![];
        for &a in alphabet {
            let next: BTreeSet<usize> = sets[i].iter().flat_map(|&j| succ(j).iter().copied())
                .filter(|&k| g.letters[k - 1] == a).collect();
            let n = sets.len();
            let k = *index.entry(next.clone()).or_insert_with(|| {
                sets.push(next);
                todo.push_back(n);
                n
            });
            row.push(k);
        }
        delta.push(row);
    }
    let accept = sets.iter()
        .map(|s| s.iter().any(|&j| if j == 0 { g.nullable } else { g.last.contains(&j) }))
        .collect();
    Dfa { alphabet: alphabet.to_vec(), delta, accept }
}

/// Moore: start from {accepting, other}; split classes by the classes of the successors
/// until nothing splits. Returns the class of each state after each round.
pub fn moore(d: &Dfa) -> Vec<Vec<usize>> {
    let renumber = |keys: Vec<Vec<usize>>| {
        let mut seen = HashMap::new();
        keys.into_iter().map(|k| {
            let n = seen.len();
            *seen.entry(k).or_insert(n) // a new key gets the next number
        }).collect()
    };
    let first = d.accept.iter().map(|&a| vec![a as usize]).collect();
    let mut rounds: Vec<Vec<usize>> = vec![renumber(first)];
    loop {
        let class = rounds.last().unwrap();
        let keys = (0..d.delta.len())
            .map(|q| {
                let succ = d.delta[q].iter().map(|&r| class[r]);
                std::iter::once(class[q]).chain(succ).collect() // own class, then successors'
            })
            .collect();
        let next: Vec<usize> = renumber(keys);
        let count = |c: &Vec<usize>| c.iter().max().map_or(0, |m| m + 1);
        if count(&next) == count(class) {
            return rounds; // stable: the classes are those of the minimal automaton
        }
        rounds.push(next);
    }
}

/// The quotient by the final classes: the minimal automaton (start class 0).
pub fn minimise(d: &Dfa) -> Dfa {
    let class = moore(d).pop().unwrap();
    let n = class.iter().max().unwrap() + 1;
    let (mut delta, mut accept) = (vec![vec![]; n], vec![false; n]);
    for q in 0..d.delta.len() {
        delta[class[q]] = d.delta[q].iter().map(|&r| class[r]).collect();
        accept[class[q]] = d.accept[q];
    }
    Dfa { alphabet: d.alphabet.clone(), delta, accept }
}

/// None if the two automata recognise the same language, else a shortest word on which
/// they differ: a breadth-first search over the pairs of states.
pub fn difference(x: &Dfa, y: &Dfa) -> Option<String> {
    let mut seen = HashMap::from([((0, 0), String::new())]);
    let mut todo = VecDeque::from([(0, 0)]);
    while let Some((p, q)) = todo.pop_front() {
        let w = seen[&(p, q)].clone();
        if x.accept[p] != y.accept[q] {
            return Some(w);
        }
        for (a, &c) in x.alphabet.iter().enumerate() {
            let next = (x.delta[p][a], y.delta[q][a]);
            if let std::collections::hash_map::Entry::Vacant(e) = seen.entry(next) {
                e.insert(format!("{w}{c}")); // a shortest word reaching this pair
                todo.push_back(next);
            }
        }
    }
    None
}

/// State elimination: edges labelled by expressions, a new start S and end E; remove
/// the states one by one, rerouting every path through the removed state.
pub fn eliminate(d: &Dfa) -> Re {
    let n = d.delta.len();
    let (s, e) = (n, n + 1);
    let mut r = vec![vec![Re::Empty; n + 2]; n + 2];
    for (q, row) in d.delta.iter().enumerate() {
        for (a, &t) in row.iter().enumerate() {
            r[q][t] = alt(r[q][t].clone(), Re::Char(d.alphabet[a]));
        }
        if d.accept[q] {
            r[q][e] = Re::Eps;
        }
    }
    r[s][0] = Re::Eps;
    for k in 0..n {
        let loop_k = star(r[k][k].clone());
        for i in k + 1..n + 2 {
            for j in k + 1..n + 2 {
                let through = cat(cat(r[i][k].clone(), loop_k.clone()), r[k][j].clone());
                r[i][j] = alt(r[i][j].clone(), through); // i -> k, loops on k, k -> j
            }
        }
    }
    r[s][e].clone()
}
