// automaton.rs: deterministic and nondeterministic finite automata over a small alphabet.
use std::collections::{BTreeSet, HashMap, VecDeque};

pub struct Dfa {
    pub alphabet: Vec<char>,
    pub delta: Vec<Vec<Option<usize>>>, // delta[q][letter index]; None: no transition
    pub start: usize,
    pub accept: Vec<bool>,
}

impl Dfa {
    pub fn letter(&self, c: char) -> Option<usize> {
        self.alphabet.iter().position(|&a| a == c)
    }

    /// The extended transition function: the state after reading the whole word.
    pub fn run_from(&self, q: usize, word: &str) -> Option<usize> {
        word.chars().try_fold(q, |q, c| self.delta[q][self.letter(c)?])
    }

    pub fn accepts(&self, word: &str) -> bool {
        self.run_from(self.start, word).is_some_and(|q| self.accept[q])
    }

    /// Add a sink state that receives every missing transition.
    pub fn complete(&self) -> Dfa {
        let sink = self.delta.len();
        let mut delta: Vec<Vec<Option<usize>>> = self.delta.iter()
            .map(|row| row.iter().map(|t| Some(t.unwrap_or(sink))).collect())
            .collect();
        delta.push(vec![Some(sink); self.alphabet.len()]);
        let mut accept = self.accept.clone();
        accept.push(false);
        Dfa { alphabet: self.alphabet.clone(), delta, start: self.start, accept }
    }

    /// Swap accepting and other states of the completed automaton.
    pub fn complement(&self) -> Dfa {
        let mut d = self.complete();
        d.accept.iter_mut().for_each(|a| *a = !*a);
        d
    }

    /// States reachable from the start (accessible).
    pub fn accessible(&self) -> Vec<bool> {
        let mut seen = vec![false; self.delta.len()];
        let mut todo = vec![self.start];
        seen[self.start] = true;
        while let Some(q) = todo.pop() {
            for &r in self.delta[q].iter().flatten() {
                if !seen[r] {
                    seen[r] = true;
                    todo.push(r);
                }
            }
        }
        seen
    }

    /// States from which an accepting state can be reached (co-accessible).
    pub fn co_accessible(&self) -> Vec<bool> {
        let mut good = self.accept.clone();
        let mut changed = true;
        while changed {
            changed = false;
            for q in 0..self.delta.len() {
                if !good[q] && self.delta[q].iter().flatten().any(|&r| good[r]) {
                    good[q] = true;
                    changed = true;
                }
            }
        }
        good
    }

    /// Number of accepted words of each length 0..=n, by dynamic programming.
    pub fn count_accepted(&self, n: usize) -> Vec<u64> {
        let mut ways = vec![0u64; self.delta.len()]; // words leading to each state
        ways[self.start] = 1;
        let mut counts = Vec::new();
        for _ in 0..=n {
            counts.push((0..ways.len()).filter(|&q| self.accept[q]).map(|q| ways[q]).sum());
            let mut next = vec![0u64; ways.len()];
            for (q, row) in self.delta.iter().enumerate() {
                for &r in row.iter().flatten() {
                    next[r] += ways[q];
                }
            }
            ways = next;
        }
        counts
    }
}

pub struct Nfa {
    pub alphabet: Vec<char>,
    pub delta: Vec<Vec<Vec<usize>>>, // delta[q][letter index]: a set of states
    pub eps: Vec<Vec<usize>>,        // spontaneous transitions
    pub start: Vec<usize>,
    pub accept: Vec<bool>,
}

pub type Subset = BTreeSet<usize>;

impl Nfa {
    /// The states reachable from the set by spontaneous transitions: a graph search.
    pub fn closure(&self, set: &Subset) -> Subset {
        let mut out = set.clone();
        let mut todo: Vec<usize> = set.iter().copied().collect();
        while let Some(q) = todo.pop() {
            for &r in &self.eps[q] {
                if out.insert(r) {
                    todo.push(r); // new: its own spontaneous moves follow
                }
            }
        }
        out
    }

    /// One letter from a closed set of states, then the closure.
    pub fn step(&self, set: &Subset, a: usize) -> Subset {
        let next = set.iter().flat_map(|&q| self.delta[q][a].iter().copied()).collect();
        self.closure(&next)
    }

    /// Simulation on the fly: the set of states the automaton may be in.
    pub fn accepts(&self, word: &str) -> bool {
        let mut set = self.closure(&self.start.iter().copied().collect());
        for c in word.chars() {
            match self.alphabet.iter().position(|&a| a == c) {
                Some(a) => set = self.step(&set, a),
                None => return false,
            }
        }
        set.iter().any(|&q| self.accept[q])
    }

    /// The subset construction, from the start set, keeping accessible subsets only.
    pub fn determinise(&self) -> (Dfa, Vec<Subset>) {
        let first = self.closure(&self.start.iter().copied().collect());
        let mut index = HashMap::from([(first.clone(), 0)]);
        let (mut subsets, mut delta) = (vec![first], Vec::new());
        let mut todo = VecDeque::from([0]);
        while let Some(i) = todo.pop_front() {
            let mut row = Vec::new();
            for a in 0..self.alphabet.len() {
                let target = self.step(&subsets[i], a);
                let j = *index.entry(target.clone()).or_insert_with(|| {
                    subsets.push(target);
                    todo.push_back(subsets.len() - 1);
                    subsets.len() - 1
                });
                row.push(Some(j));
            }
            delta.push(row);
        }
        let accept = subsets.iter().map(|s| s.iter().any(|&q| self.accept[q])).collect();
        (Dfa { alphabet: self.alphabet.clone(), delta, start: 0, accept }, subsets)
    }
}

/// "The k-th letter from the end is a", over {a, b}: k + 1 states.
pub fn kth_from_end(k: usize) -> Nfa {
    let mut delta = vec![vec![vec![], vec![]]; k + 1];
    delta[0] = vec![vec![0, 1], vec![0]]; // guess where the a is
    for (q, row) in delta.iter_mut().enumerate().take(k).skip(1) {
        *row = vec![vec![q + 1], vec![q + 1]];
    }
    let mut accept = vec![false; k + 1];
    accept[k] = true;
    Nfa { alphabet: vec!['a', 'b'], delta, eps: vec![vec![]; k + 1], start: vec![0], accept }
}

/// The product of two complete automata on the same alphabet; both: intersection.
pub fn product(x: &Dfa, y: &Dfa, both: bool) -> Dfa {
    let m = y.delta.len();
    let pair = |p: usize, q: usize| p * m + q;
    let mut delta = Vec::new();
    let mut accept = Vec::new();
    for p in 0..x.delta.len() {
        for q in 0..m {
            delta.push((0..x.alphabet.len())
                .map(|a| Some(pair(x.delta[p][a]?, y.delta[q][a]?)))
                .collect());
            let (u, v) = (x.accept[p], y.accept[q]);
            accept.push(if both { u && v } else { u || v });
        }
    }
    Dfa { alphabet: x.alphabet.clone(), delta, start: pair(x.start, y.start), accept }
}
