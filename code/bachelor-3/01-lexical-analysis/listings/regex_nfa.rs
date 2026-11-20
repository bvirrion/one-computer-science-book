// regex_nfa.rs -- regular expressions over ASCII and Thompson's construction.
#![allow(dead_code)]

/// A regular expression. A set of characters is a list of ranges.
#[derive(Clone, Debug)]
pub enum Re {
    Eps,
    Set(Vec<(u8, u8)>),
    Cat(Box<Re>, Box<Re>),
    Alt(Box<Re>, Box<Re>),
    Star(Box<Re>),
    Plus(Box<Re>),
    Opt(Box<Re>),
}

/// Parse `|`, `*`, `+`, `?`, `( )`, `[a-z0-9_]`, `[^\n]` and `\` escapes.
pub fn parse(s: &str) -> Result<Re, String> {
    let mut p = Parser { s: s.as_bytes(), i: 0 };
    let re = p.alt()?;
    match p.s.get(p.i) {
        None => Ok(re),
        Some(c) => Err(format!("unexpected '{}' at {}", *c as char, p.i)),
    }
}

struct Parser<'a> {
    s: &'a [u8],
    i: usize,
}

impl Parser<'_> {
    fn alt(&mut self) -> Result<Re, String> {
        let mut left = self.cat()?;
        while self.s.get(self.i) == Some(&b'|') {
            self.i += 1;
            left = Re::Alt(Box::new(left), Box::new(self.cat()?));
        }
        Ok(left)
    }
    fn cat(&mut self) -> Result<Re, String> {
        let mut parts = Vec::new();
        while let Some(&c) = self.s.get(self.i) {
            if c == b'|' || c == b')' {
                break;
            }
            parts.push(self.post()?);
        }
        let mut it = parts.into_iter();
        let first = it.next().unwrap_or(Re::Eps);
        Ok(it.fold(first, |a, b| Re::Cat(Box::new(a), Box::new(b))))
    }
    fn post(&mut self) -> Result<Re, String> {
        let mut r = self.atom()?;
        while let Some(&c) = self.s.get(self.i) {
            r = match c {
                b'*' => Re::Star(Box::new(r)),
                b'+' => Re::Plus(Box::new(r)),
                b'?' => Re::Opt(Box::new(r)),
                _ => break,
            };
            self.i += 1;
        }
        Ok(r)
    }
    fn atom(&mut self) -> Result<Re, String> {
        let c = self.s[self.i];
        self.i += 1;
        match c {
            b'(' => {
                let r = self.alt()?;
                if self.s.get(self.i) != Some(&b')') {
                    return Err("missing ')'".into());
                }
                self.i += 1;
                Ok(r)
            }
            b'[' => self.class(),
            b'\\' => {
                let c = self.escape();
                Ok(Re::Set(vec![(c, c)]))
            }
            b'*' | b'+' | b'?' => Err(format!("nothing to repeat at {}", self.i - 1)),
            _ => Ok(Re::Set(vec![(c, c)])),
        }
    }
    fn escape(&mut self) -> u8 {
        let c = self.s[self.i];
        self.i += 1;
        if c == b'n' { b'\n' } else if c == b't' { b'\t' } else { c }
    }
    fn class(&mut self) -> Result<Re, String> {
        let negate = self.s.get(self.i) == Some(&b'^');
        if negate {
            self.i += 1;
        }
        let mut ranges = Vec::new();
        while let Some(&c) = self.s.get(self.i) {
            if c == b']' {
                self.i += 1;
                return Ok(Re::Set(if negate { complement(&ranges) } else { ranges }));
            }
            self.i += 1;
            let lo = if c == b'\\' { self.escape() } else { c };
            let hi = if self.s.get(self.i) == Some(&b'-') && self.s.get(self.i + 1) != Some(&b']') {
                self.i += 2;
                self.s[self.i - 1]
            } else {
                lo
            };
            ranges.push((lo, hi));
        }
        Err("missing ']'".into())
    }
}

fn complement(ranges: &[(u8, u8)]) -> Vec<(u8, u8)> {
    let inside = |c: u8| ranges.iter().any(|&(lo, hi)| lo <= c && c <= hi);
    let mut out: Vec<(u8, u8)> = Vec::new();
    for c in 0..128u8 {
        if inside(c) {
            continue;
        }
        match out.last_mut() {
            Some(last) if last.1 + 1 == c => last.1 = c,
            _ => out.push((c, c)),
        }
    }
    out
}

/// An NFA state: its epsilon moves and its moves on a range of characters.
#[derive(Default, Clone, Debug)]
pub struct State {
    pub eps: Vec<usize>,
    pub moves: Vec<(u8, u8, usize)>,
    pub accept: Option<usize>, // the rule this state accepts, if any
}

#[derive(Default, Debug)]
pub struct Nfa {
    pub states: Vec<State>,
    pub start: usize,
}

impl Nfa {
    fn new_state(&mut self) -> usize {
        self.states.push(State::default());
        self.states.len() - 1
    }

    /// Thompson's construction: a fragment with one entry and one exit.
    pub fn fragment(&mut self, re: &Re) -> (usize, usize) {
        if let Re::Cat(a, b) = re {
            let (a_in, a_out) = self.fragment(a);
            let (b_in, b_out) = self.fragment(b);
            self.states[a_out].eps.push(b_in); // concatenation adds no state
            return (a_in, b_out);
        }
        let (s, e) = (self.new_state(), self.new_state());
        match re {
            Re::Eps => self.states[s].eps.push(e),
            Re::Set(ranges) => {
                for &(lo, hi) in ranges {
                    self.states[s].moves.push((lo, hi, e));
                }
            }
            Re::Alt(a, b) => {
                for r in [a, b] {
                    let (i, o) = self.fragment(r);
                    self.states[s].eps.push(i);
                    self.states[o].eps.push(e);
                }
            }
            Re::Star(a) | Re::Plus(a) | Re::Opt(a) => {
                let (i, o) = self.fragment(a);
                self.states[s].eps.push(i);
                self.states[o].eps.push(e);
                if !matches!(re, Re::Plus(_)) {
                    self.states[s].eps.push(e); // zero times
                }
                if !matches!(re, Re::Opt(_)) {
                    self.states[o].eps.push(i); // once more
                }
            }
            Re::Cat(..) => unreachable!(),
        }
        (s, e)
    }
}

/// The scanner's NFA: a new start state with an epsilon move into each
/// rule's fragment; the exit of rule k accepts k.
pub fn union(rules: &[&str]) -> Result<Nfa, String> {
    let mut nfa = Nfa::default();
    nfa.start = nfa.new_state();
    for (k, rule) in rules.iter().enumerate() {
        let (i, o) = nfa.fragment(&parse(rule)?);
        nfa.states[nfa.start].eps.push(i);
        nfa.states[o].accept = Some(k);
    }
    Ok(nfa)
}
