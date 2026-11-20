// pda.rs: pushdown automata, run by a bounded search over configurations.
use crate::grammar::{Grammar, Sym};
use std::collections::HashSet;

/// In state `from`, reading `read` (or nothing), with `pop` on top of the stack: go to
/// state `to` and replace `pop` by `push`, whose first symbol ends on top.
pub struct Move {
    pub from: usize,
    pub read: Option<char>,
    pub pop: char,
    pub to: usize,
    pub push: Vec<char>,
}

pub struct Pda {
    pub start: usize,
    pub bottom: char, // the only symbol on the stack at the start
    pub accept: Vec<usize>,
    pub moves: Vec<Move>,
}

impl Pda {
    /// Accepted if some run reads the whole word and ends in an accepting state. The search
    /// ignores configurations whose stack is longer than `limit`; it returns the answer
    /// and the number of configurations visited.
    pub fn accepts(&self, word: &str, limit: usize) -> (bool, usize) {
        let w: Vec<char> = word.chars().collect();
        let first = (self.start, 0, vec![self.bottom]); // state, letters read, stack
        let mut seen = HashSet::from([first.clone()]);
        let mut todo = vec![first];
        while let Some((q, i, stack)) = todo.pop() {
            if i == w.len() && self.accept.contains(&q) {
                return (true, seen.len());
            }
            let Some(&top) = stack.last() else { continue }; // an empty stack blocks
            for m in self.moves.iter().filter(|m| m.from == q && m.pop == top) {
                let j = match m.read {
                    None => i,
                    Some(c) if w.get(i) == Some(&c) => i + 1,
                    Some(_) => continue,
                };
                let mut next = stack[..stack.len() - 1].to_vec();
                next.extend(m.push.iter().rev()); // push's first symbol on top
                if next.len() <= limit && seen.insert((m.to, j, next.clone())) {
                    todo.push((m.to, j, next));
                }
            }
        }
        (false, seen.len())
    }

    /// The automaton of a grammar whose nonterminals are single letters: put S on the
    /// stack; replace a nonterminal on top by a right side; match a terminal on top with
    /// the next letter; accept when only the bottom is left.
    pub fn from_grammar(g: &Grammar) -> Pda {
        let letter = |s: &Sym| match s {
            Sym::T(c) => *c,
            Sym::N(a) => a.chars().next().unwrap(),
        };
        let mut moves = vec![Move { from: 0, read: None, pop: '$', to: 1,
                                    push: vec![letter(&Sym::N(g.start.clone())), '$'] }];
        for (a, rhs) in &g.rules { // expand: the nonterminal a becomes the right side
            let (pop, push) = (letter(&Sym::N(a.clone())), rhs.iter().map(letter).collect());
            moves.push(Move { from: 1, read: None, pop, to: 1, push });
        }
        let terminals: HashSet<char> = g.rules.iter().flat_map(|(_, rhs)| rhs.iter())
            .filter_map(|s| match s { Sym::T(c) => Some(*c), _ => None }).collect();
        for c in terminals {
            moves.push(Move { from: 1, read: Some(c), pop: c, to: 1, push: vec![] });
        }
        moves.push(Move { from: 1, read: None, pop: '$', to: 2, push: vec![] });
        Pda { start: 0, bottom: '$', accept: vec![2], moves }
    }
}
