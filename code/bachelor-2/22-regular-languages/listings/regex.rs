// regex.rs: regular expressions: syntax, parser, denotation, and Glushkov's positions.
use std::collections::BTreeSet;

#[derive(Clone, Debug, PartialEq)]
pub enum Re {
    Empty, // the empty language
    Eps,   // the empty word
    Char(char),
    Cat(Box<Re>, Box<Re>),
    Alt(Box<Re>, Box<Re>),
    Star(Box<Re>),
}

pub fn cat(x: Re, y: Re) -> Re {
    match (x, y) {
        (Re::Empty, _) | (_, Re::Empty) => Re::Empty,
        (Re::Eps, r) | (r, Re::Eps) => r,
        (x, y) => Re::Cat(Box::new(x), Box::new(y)),
    }
}

pub fn alt(x: Re, y: Re) -> Re {
    match (x, y) {
        (Re::Empty, r) | (r, Re::Empty) => r,
        (x, y) if x == y => x,
        (x, y) => Re::Alt(Box::new(x), Box::new(y)),
    }
}

pub fn star(x: Re) -> Re {
    match x {
        Re::Empty | Re::Eps => Re::Eps,
        Re::Star(r) => Re::Star(r),
        r => Re::Star(Box::new(r)),
    }
}

impl Re {
    /// The expression as text, with only the brackets that priorities require.
    pub fn show(&self) -> String {
        let wrap = |r: &Re, level: u8| {
            let p = match r { Re::Alt(..) => 0, Re::Cat(..) => 1, _ => 2 };
            if p < level { format!("({})", r.show()) } else { r.show() }
        };
        match self {
            Re::Empty => "∅".into(),
            Re::Eps => "ε".into(),
            Re::Char(c) => c.to_string(),
            Re::Cat(x, y) => format!("{}{}", wrap(x, 1), wrap(y, 1)),
            Re::Alt(x, y) => format!("{}|{}", x.show(), y.show()),
            Re::Star(x) => format!("{}*", wrap(x, 2)),
        }
    }
}

/// Parse: alt := cat ('|' cat)*; cat := post*; post := atom ('*' | '+' | '?' | {m,n})*;
/// atom := letter | '(' alt ')' | '[' letters ']' | 'ε'.
pub fn parse(text: &str) -> Result<Re, String> {
    let chars: Vec<char> = text.chars().collect();
    let mut pos = 0;
    let re = parse_alt(&chars, &mut pos)?;
    if pos < chars.len() {
        return Err(format!("unexpected '{}' at {pos}", chars[pos]));
    }
    Ok(re)
}

fn parse_alt(s: &[char], pos: &mut usize) -> Result<Re, String> {
    let mut re = parse_cat(s, pos)?;
    while *pos < s.len() && s[*pos] == '|' {
        *pos += 1;
        re = Re::Alt(Box::new(re), Box::new(parse_cat(s, pos)?));
    }
    Ok(re)
}

fn parse_cat(s: &[char], pos: &mut usize) -> Result<Re, String> {
    let mut re = Re::Eps;
    while *pos < s.len() && s[*pos] != '|' && s[*pos] != ')' {
        let next = parse_post(s, pos)?;
        re = if re == Re::Eps { next } else { Re::Cat(Box::new(re), Box::new(next)) };
    }
    Ok(re)
}

fn parse_post(s: &[char], pos: &mut usize) -> Result<Re, String> {
    let mut re = parse_atom(s, pos)?;
    while *pos < s.len() {
        re = match s[*pos] {
            '*' => Re::Star(Box::new(re)),
            '+' => Re::Cat(Box::new(re.clone()), Box::new(Re::Star(Box::new(re)))), // xx*
            '?' => Re::Alt(Box::new(re), Box::new(Re::Eps)), // x|ε
            '{' => {
                let close = s[*pos..].iter().position(|&c| c == '}').ok_or("no '}'")? + *pos;
                let body: String = s[*pos + 1..close].iter().collect();
                let (m, n) = match body.split_once(',') {
                    Some((m, n)) => (m.parse(), n.parse()),
                    None => (body.parse(), body.parse()),
                };
                let bad = |_| "bad count";
                let (m, n): (usize, usize) = (m.map_err(bad)?, n.map_err(bad)?);
                *pos = close;
                repeat(&re, m, n) // m copies, then n - m optional ones
            }
            _ => break,
        };
        *pos += 1;
    }
    Ok(re)
}

fn repeat(re: &Re, m: usize, n: usize) -> Re {
    let mut out = Re::Eps;
    for i in 0..n {
        let optional = || Re::Alt(Box::new(re.clone()), Box::new(Re::Eps));
        let copy = if i < m { re.clone() } else { optional() };
        out = if out == Re::Eps { copy } else { Re::Cat(Box::new(out), Box::new(copy)) };
    }
    out
}

fn parse_atom(s: &[char], pos: &mut usize) -> Result<Re, String> {
    let c = *s.get(*pos).ok_or("expression ends too early")?;
    *pos += 1;
    match c {
        '(' => {
            let re = parse_alt(s, pos)?;
            if s.get(*pos) != Some(&')') {
                return Err(format!("missing ')' at {}", *pos));
            }
            *pos += 1;
            Ok(re)
        }
        '[' => { // a class: one letter among those listed
            let close = s[*pos..].iter().position(|&c| c == ']').ok_or("no ']'")? + *pos;
            let (body, mut letters) = (&s[*pos..close], vec![]);
            let mut k = 0;
            while k < body.len() {
                if k + 2 < body.len() && body[k + 1] == '-' { // a range such as a-z
                    letters.extend(body[k]..=body[k + 2]);
                    k += 3;
                } else {
                    letters.push(body[k]);
                    k += 1;
                }
            }
            let re = letters.into_iter().map(Re::Char)
                .reduce(|x, y| Re::Alt(Box::new(x), Box::new(y)))
                .ok_or("empty class")?;
            *pos = close + 1;
            Ok(re)
        }
        'ε' => Ok(Re::Eps),
        '*' | '+' | '?' | ')' | '|' | '{' => Err(format!("unexpected '{c}' at {}", *pos - 1)),
        c => Ok(Re::Char(c)),
    }
}

/// The denotation, cut to the words of length at most n: the definition, run.
pub fn lang(re: &Re, n: usize) -> BTreeSet<String> {
    match re {
        Re::Empty => BTreeSet::new(),
        Re::Eps => BTreeSet::from([String::new()]),
        Re::Char(c) => if n >= 1 { BTreeSet::from([c.to_string()]) } else { BTreeSet::new() },
        Re::Alt(x, y) => lang(x, n).union(&lang(y, n)).cloned().collect(),
        Re::Cat(x, y) => {
            let (lx, ly) = (lang(x, n), lang(y, n));
            lx.iter().flat_map(|u| ly.iter().filter(move |v| u.len() + v.len() <= n)
                .map(move |v| format!("{u}{v}"))).collect()
        }
        Re::Star(x) => {
            let lx = lang(x, n);
            let mut all = BTreeSet::from([String::new()]);
            let mut frontier = all.clone();
            while !frontier.is_empty() { // add one more factor until nothing new fits
                let next: BTreeSet<String> = frontier.iter()
                    .flat_map(|u| lx.iter().filter(move |v| u.len() + v.len() <= n)
                        .map(move |v| format!("{u}{v}")))
                    .filter(|w| !all.contains(w)).collect();
                all.extend(next.iter().cloned());
                frontier = next;
            }
            all
        }
    }
}

/// Glushkov's positions: the letters of the expression numbered 1..=m from the left.
pub struct Glushkov {
    pub letters: Vec<char>, // letters[j - 1]: the letter at position j
    pub nullable: bool,     // is ε in the language?
    pub first: BTreeSet<usize>,
    pub last: BTreeSet<usize>,
    pub follow: Vec<BTreeSet<usize>>, // follow[j]: positions that may come after j
}

pub fn glushkov(re: &Re) -> Glushkov {
    let mut g = Glushkov { letters: vec![], nullable: false, first: BTreeSet::new(),
                           last: BTreeSet::new(), follow: vec![BTreeSet::new()] };
    let (nullable, first, last) = walk(re, &mut g);
    (g.nullable, g.first, g.last) = (nullable, first, last);
    g
}

type Sets = (bool, BTreeSet<usize>, BTreeSet<usize>);

/// Berry and Sethi: nullable, first and last of each subexpression, bottom up,
/// adding to follow at each concatenation and each star.
fn walk(re: &Re, g: &mut Glushkov) -> Sets {
    let none = BTreeSet::new;
    match re {
        Re::Empty => (false, none(), none()),
        Re::Eps => (true, none(), none()),
        Re::Char(c) => {
            g.letters.push(*c);
            g.follow.push(none());
            let j = g.letters.len(); // the next position
            (false, BTreeSet::from([j]), BTreeSet::from([j]))
        }
        Re::Alt(x, y) => {
            let ((nx, fx, lx), (ny, fy, ly)) = (walk(x, g), walk(y, g));
            (nx || ny, &fx | &fy, &lx | &ly)
        }
        Re::Cat(x, y) => {
            let ((nx, fx, lx), (ny, fy, ly)) = (walk(x, g), walk(y, g));
            for &j in &lx {
                g.follow[j].extend(fy.iter()); // the end of x, then the start of y
            }
            let first = if nx { &fx | &fy } else { fx };
            let last = if ny { &lx | &ly } else { ly };
            (nx && ny, first, last)
        }
        Re::Star(x) => {
            let (_, fx, lx) = walk(x, g);
            for &j in &lx {
                g.follow[j].extend(fx.iter()); // the end of x, then x again
            }
            (true, fx, lx)
        }
    }
}

/// The Glushkov automaton run on sets of states held in the bits of a u128:
/// state 0 is the start, state j the position j.
pub struct Matcher {
    succ: Vec<u128>,                             // succ[i]: first (i = 0) or follow(i)
    with: std::collections::HashMap<char, u128>, // the positions holding each letter
    accept: u128,
}

impl Matcher {
    pub fn new(g: &Glushkov) -> Matcher {
        assert!(g.letters.len() < 128, "at most 127 positions");
        let bits = |s: &BTreeSet<usize>| s.iter().fold(0u128, |m, &j| m | 1 << j);
        let mut succ = vec![bits(&g.first)];
        succ.extend(g.follow[1..].iter().map(bits));
        let mut with = std::collections::HashMap::new();
        for (j, &c) in g.letters.iter().enumerate() {
            *with.entry(c).or_insert(0) |= 1u128 << (j + 1);
        }
        Matcher { succ, with, accept: bits(&g.last) | g.nullable as u128 }
    }

    /// Accept or not, and the number of steps: at most m + 1 ORs per letter.
    pub fn run(&self, word: &str) -> (bool, usize) {
        let (mut set, mut steps) = (1u128, 0); // {0}
        for c in word.chars() {
            let mut next = 0;
            let mut rest = set;
            while rest != 0 {
                next |= self.succ[rest.trailing_zeros() as usize];
                rest &= rest - 1;
                steps += 1;
            }
            set = next & self.with.get(&c).copied().unwrap_or(0);
        }
        (set & self.accept != 0, steps)
    }

    pub fn matches(&self, word: &str) -> bool {
        self.run(word).0
    }
}
