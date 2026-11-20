// thompson.rs: Thompson's construction, state counts against Glushkov's m + 1.
#[allow(dead_code)]
mod regex;
use regex::Re;
use std::collections::BTreeSet;

#[derive(Default)]
struct Nfa {
    eps: Vec<Vec<usize>>,               // spontaneous transitions
    letter: Vec<Option<(char, usize)>>, // at most one letter transition per state
}

impl Nfa {
    fn state(&mut self) -> usize {
        self.eps.push(vec![]);
        self.letter.push(None);
        self.eps.len() - 1
    }

    /// A fragment with one entry and one exit for the expression.
    fn build(&mut self, re: &Re) -> (usize, usize) {
        let (i, o) = (self.state(), self.state());
        match re {
            Re::Empty => {}
            Re::Eps => self.eps[i].push(o),
            Re::Char(c) => self.letter[i] = Some((*c, o)),
            Re::Cat(x, y) => {
                let ((xi, xo), (yi, yo)) = (self.build(x), self.build(y));
                self.eps[i].push(xi);
                self.eps[xo].push(yi);
                self.eps[yo].push(o);
            }
            Re::Alt(x, y) => {
                let ((xi, xo), (yi, yo)) = (self.build(x), self.build(y));
                self.eps[i].extend([xi, yi]);
                self.eps[xo].push(o);
                self.eps[yo].push(o);
            }
            Re::Star(x) => {
                let (xi, xo) = self.build(x);
                self.eps[i].extend([xi, o]); // enter x, or skip it
                self.eps[xo].extend([xi, o]); // again, or leave
            }
        }
        (i, o)
    }

    fn closure(&self, mut set: BTreeSet<usize>) -> BTreeSet<usize> {
        let mut todo: Vec<usize> = set.iter().copied().collect();
        while let Some(q) = todo.pop() {
            for &r in &self.eps[q] {
                if set.insert(r) {
                    todo.push(r);
                }
            }
        }
        set
    }

    fn accepts(&self, (i, o): (usize, usize), word: &str) -> bool {
        let mut set = self.closure(BTreeSet::from([i]));
        for c in word.chars() {
            let next = set.iter().filter_map(|&q| match self.letter[q] {
                Some((d, r)) if d == c => Some(r),
                _ => None,
            }).collect();
            set = self.closure(next);
        }
        set.contains(&o)
    }
}

fn main() {
    println!("expression          Thompson states  Glushkov states  agree up to length 7");
    for text in ["(a|b)*abb", "a*b*c*", "(ab|b)*", "((a|b)(a|b))*", "a?b?c"] {
        let re = regex::parse(text).unwrap();
        let mut nfa = Nfa::default();
        let ends = nfa.build(&re);
        let g = regex::glushkov(&re);
        let m = regex::Matcher::new(&g);
        let all = regex::lang(&regex::parse("(a|b|c)*").unwrap(), 7);
        let agree = all.iter().all(|w| nfa.accepts(ends, w) == m.matches(w));
        println!("{text:19} {:15}  {:15}  {agree}", nfa.eps.len(), g.letters.len() + 1);
    }
}
