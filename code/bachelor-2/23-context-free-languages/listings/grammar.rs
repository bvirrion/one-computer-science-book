// grammar.rs: context-free grammars: rules, generated words, derivations, CNF, CYK.
use std::collections::{BTreeSet, HashMap, HashSet, VecDeque};

/// A symbol: a terminal (one character) or a nonterminal (a name).
#[derive(Clone, Debug, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Sym {
    T(char),
    N(String),
}

#[derive(Clone)]
pub struct Grammar {
    pub start: String,
    pub rules: Vec<(String, Vec<Sym>)>, // A -> X1 ... Xk; an empty right side is ε
}

pub fn show(form: &[Sym]) -> String {
    if form.is_empty() {
        return "ε".into();
    }
    let names: Vec<String> = form.iter().map(|s| match s {
        Sym::T(c) => c.to_string(),
        Sym::N(a) => a.clone(),
    }).collect();
    names.join(" ")
}

impl Grammar {
    /// "E -> E + T | T" on each line; a name starting with a capital is a nonterminal,
    /// ε is the empty right side, the first rule's left side is the start symbol.
    pub fn parse(text: &str) -> Grammar {
        let mut rules = vec![];
        for line in text.lines().filter(|l| l.contains("->")) {
            let (lhs, rhs) = line.split_once("->").unwrap();
            for alternative in rhs.split(" | ") {
                let syms = alternative.split_whitespace().filter(|&t| t != "ε").map(|t| {
                    if t.starts_with(|c: char| c.is_ascii_uppercase()) {
                        Sym::N(t.to_string())
                    } else {
                        assert_eq!(t.chars().count(), 1, "a terminal is one character: {t}");
                        Sym::T(t.chars().next().unwrap())
                    }
                });
                rules.push((lhs.trim().to_string(), syms.collect()));
            }
        }
        Grammar { start: rules[0].0.clone(), rules }
    }

    /// One line per nonterminal, its right sides separated by |.
    pub fn show(&self) -> String {
        let mut order: Vec<&String> = vec![];
        for (a, _) in &self.rules {
            if !order.contains(&a) {
                order.push(a);
            }
        }
        let line = |a: &String| {
            let sides: Vec<String> = self.rules.iter().filter(|(b, _)| b == a)
                .map(|(_, rhs)| show(rhs)).collect();
            format!("{a} -> {}", sides.join(" | "))
        };
        order.into_iter().map(line).collect::<Vec<_>>().join("\n")
    }

    pub fn nonterminals(&self) -> BTreeSet<String> {
        self.rules.iter().map(|(a, _)| a.clone()).collect()
    }

    /// The nonterminals that derive ε: a fixed point.
    pub fn nullable(&self) -> HashSet<String> {
        let mut null = HashSet::new();
        loop {
            let before = null.len();
            for (a, rhs) in &self.rules {
                if rhs.iter().all(|s| matches!(s, Sym::N(b) if null.contains(b))) {
                    null.insert(a.clone());
                }
            }
            if null.len() == before {
                return null;
            }
        }
    }

    /// The words of length at most n that each nonterminal derives: the least fixed point
    /// of "A derives the concatenations of what its right sides' symbols derive".
    pub fn words(&self, n: usize) -> HashMap<String, BTreeSet<String>> {
        let mut lang: HashMap<String, BTreeSet<String>> =
            self.nonterminals().into_iter().map(|a| (a, BTreeSet::new())).collect();
        loop {
            let mut changed = false;
            for (a, rhs) in &self.rules {
                let mut acc = BTreeSet::from([String::new()]);
                for s in rhs {
                    let part = match s {
                        Sym::T(c) => BTreeSet::from([c.to_string()]),
                        Sym::N(b) => lang[b].clone(),
                    };
                    acc = acc.iter().flat_map(|u| part.iter()
                        .filter(move |v| u.len() + v.len() <= n)
                        .map(move |v| format!("{u}{v}"))).collect();
                }
                let set = lang.get_mut(a).unwrap();
                for w in acc {
                    changed |= set.insert(w);
                }
            }
            if !changed {
                return lang;
            }
        }
    }

    pub fn generated(&self, n: usize) -> BTreeSet<String> {
        self.words(n).remove(&self.start).unwrap()
    }

    /// A leftmost derivation of `word`, by a breadth-first search over sentential forms.
    /// A form is dropped when the terminals before its first nonterminal are not a prefix
    /// of the word, or when it has more symbols that cannot vanish than the word has letters.
    pub fn leftmost(&self, word: &str) -> Option<Vec<Vec<Sym>>> {
        let null = self.nullable();
        let letters: Vec<Sym> = word.chars().map(Sym::T).collect();
        let fits = |form: &[Sym]| {
            let done = form.iter().take_while(|s| matches!(s, Sym::T(_))).count();
            let solid = form.iter().filter(|s| !matches!(s, Sym::N(b) if null.contains(b)));
            done <= letters.len() && form[..done] == letters[..done]
                && solid.count() <= letters.len()
        };
        let start = vec![Sym::N(self.start.clone())];
        let mut parent = HashMap::from([(start.clone(), vec![])]); // the start has none
        let mut todo = VecDeque::from([start]);
        while let Some(form) = todo.pop_front() {
            if form == letters {
                let mut steps = vec![form];
                while let Some(p) = parent.get(steps.last().unwrap()) {
                    if p.is_empty() {
                        break; // the start symbol
                    }
                    steps.push(p.clone());
                }
                steps.reverse();
                return Some(steps);
            }
            let Some(k) = form.iter().position(|s| matches!(s, Sym::N(_))) else { continue };
            for (a, rhs) in &self.rules {
                if form[k] != Sym::N(a.clone()) {
                    continue; // only the rules of the leftmost nonterminal
                }
                let next: Vec<Sym> = [&form[..k], rhs, &form[k + 1..]].concat();
                if fits(&next) && !parent.contains_key(&next) {
                    parent.insert(next.clone(), form.clone());
                    todo.push_back(next);
                }
            }
        }
        None
    }

    fn fresh(&self, base: &str) -> String {
        let names = self.nonterminals();
        (0..).map(|i| format!("{base}{i}")).find(|n| !names.contains(n)).unwrap()
    }

    /// Chomsky normal form, in five steps: a new start; terminals in long right sides
    /// replaced; long right sides cut in pairs; ε-rules removed; unit rules removed.
    pub fn cnf(&self) -> Grammar {
        let mut g = self.clone();
        let start = Sym::N(self.start.clone());
        let used_inside = self.rules.iter().any(|(_, rhs)| rhs.contains(&start));
        if used_inside && self.nullable().contains(&self.start) { // START: S0 -> S, if needed
            g.start = self.fresh(&self.start);
            g.rules.insert(0, (g.start.clone(), vec![Sym::N(self.start.clone())]));
        }
        let mut out = vec![];
        for (a, rhs) in std::mem::take(&mut g.rules) { // TERM: a terminal c in A -> X Y ...
            let rhs: Vec<Sym> = rhs.iter().map(|s| match s {
                Sym::T(c) if rhs.len() >= 2 => {
                    let name = format!("'{c}'"); // ... becomes the nonterminal 'c'
                    out.push((name.clone(), vec![s.clone()]));
                    Sym::N(name)
                }
                _ => s.clone(),
            }).collect();
            out.push((a, rhs));
        }
        g.rules = out;
        let (mut out, mut used) = (vec![], g.nonterminals());
        for (a, mut rhs) in std::mem::take(&mut g.rules) { // BIN: A -> X1 Y1, Y1 -> X2 Y2 ...
            let mut lhs = a;
            while rhs.len() > 2 {
                let y = (0..).map(|i| format!("X{i}")).find(|n| !used.contains(n)).unwrap();
                used.insert(y.clone());
                out.push((lhs, vec![rhs.remove(0), Sym::N(y.clone())]));
                lhs = y;
            }
            out.push((lhs, rhs));
        }
        g.rules = out;
        let null = g.nullable(); // DEL: every way to drop nullable symbols, then no ε
        let mut out = vec![];
        for (a, rhs) in &g.rules {
            for mask in 0..1u32 << rhs.len() {
                let keep: Vec<Sym> = rhs.iter().enumerate().filter(|&(i, s)| {
                    mask >> i & 1 == 0 || !matches!(s, Sym::N(b) if null.contains(b))
                }).map(|(_, s)| s.clone()).collect();
                let rule = (a.clone(), keep);
                if (!rule.1.is_empty() || *a == g.start) && !out.contains(&rule) {
                    out.push(rule);
                }
            }
        }
        g.rules = out;
        let unit = |rhs: &[Sym]| matches!(rhs, [Sym::N(_)]); // UNIT: through unit chains
        let mut out = vec![];
        for a in g.nonterminals() {
            let mut reach = vec![a.clone()];
            let mut k = 0;
            while k < reach.len() {
                for (b, rhs) in &g.rules {
                    if *b == reach[k] && unit(rhs) {
                        if let [Sym::N(c)] = rhs.as_slice() {
                            if !reach.contains(c) {
                                reach.push(c.clone());
                            }
                        }
                    }
                }
                k += 1;
            }
            for (b, rhs) in &g.rules {
                let rule = (a.clone(), rhs.clone());
                if reach.contains(b) && !unit(rhs) && !out.contains(&rule) {
                    out.push(rule);
                }
            }
        }
        let rank = |a: &String| match self.rules.iter().position(|(b, _)| b == a) {
            _ if *a == g.start => (0, 0),
            Some(k) => (1, k),                                  // the grammar's own, in order
            None if a.starts_with('X') => (2, a[1..].parse().unwrap()), // then X0, X1 ...
            None => (3, 0),                                     // then 'a', 'b' ...
        };
        out.sort_by_key(|(a, _)| (rank(a), a.clone()));
        g.rules = out;
        g.reachable()
    }

    /// Keeps the rules of the nonterminals reachable from the start.
    pub fn reachable(&self) -> Grammar {
        let mut reach = vec![self.start.clone()];
        let mut k = 0;
        while k < reach.len() {
            let sides: Vec<Vec<Sym>> = self.rules.iter().filter(|(a, _)| *a == reach[k])
                .map(|(_, rhs)| rhs.clone()).collect();
            for s in sides.into_iter().flatten() {
                if let Sym::N(b) = s {
                    if !reach.contains(&b) {
                        reach.push(b); // used by a reachable nonterminal
                    }
                }
            }
            k += 1;
        }
        let rules = self.rules.iter().filter(|(a, _)| reach.contains(a)).cloned().collect();
        Grammar { start: self.start.clone(), rules }
    }

    /// CYK on a grammar in Chomsky normal form: table[i][l - 1] holds the nonterminals that
    /// derive the l letters from position i. Also returns the number of split points tried.
    pub fn cyk(&self, word: &str) -> (Vec<Vec<BTreeSet<String>>>, usize) {
        let w: Vec<char> = word.chars().collect();
        let n = w.len();
        let mut table = vec![vec![BTreeSet::new(); n]; n];
        for (i, &c) in w.iter().enumerate() {
            for (a, rhs) in &self.rules {
                if rhs[..] == [Sym::T(c)] {
                    table[i][0].insert(a.clone());
                }
            }
        }
        let mut splits = 0;
        for l in 2..=n {
            for i in 0..=n - l {
                for k in 1..l { // the first k letters, then the other l - k
                    splits += 1;
                    for (a, rhs) in &self.rules {
                        if let [Sym::N(b), Sym::N(c)] = rhs.as_slice() {
                            let (left, right) = (&table[i][k - 1], &table[i + k][l - k - 1]);
                            if left.contains(b) && right.contains(c) {
                                table[i][l - 1].insert(a.clone());
                            }
                        }
                    }
                }
            }
        }
        (table, splits)
    }

    pub fn accepts(&self, word: &str) -> bool {
        if word.is_empty() {
            return self.rules.iter().any(|(a, rhs)| *a == self.start && rhs.is_empty());
        }
        let (table, _) = self.cyk(word);
        table[0][word.chars().count() - 1].contains(&self.start)
    }
}
