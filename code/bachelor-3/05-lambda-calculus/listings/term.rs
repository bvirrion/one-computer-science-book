// term.rs -- pure lambda-terms with de Bruijn indices: parser from named
// syntax (\x. body), printer back to names, free variables, alpha-equivalence.
#![allow(dead_code)]
use std::collections::BTreeSet;

/// Var(k) refers to the k-th enclosing lambda (0 = the nearest); a Lam keeps its
/// variable's name only as a hint for printing.
#[derive(Clone, Debug)]
pub enum Term {
    Var(usize),
    Free(String),
    Lam(String, Box<Term>),
    App(Box<Term>, Box<Term>),
}
use Term::*;

pub fn lam(x: &str, b: Term) -> Term {
    Lam(x.to_string(), Box::new(b))
}
pub fn app(f: Term, a: Term) -> Term {
    App(Box::new(f), Box::new(a))
}

/// alpha-equivalence is equality of de Bruijn terms: names do not count.
pub fn alpha_eq(a: &Term, b: &Term) -> bool {
    match (a, b) {
        (Var(i), Var(j)) => i == j,
        (Free(x), Free(y)) => x == y,
        (Lam(_, p), Lam(_, q)) => alpha_eq(p, q),
        (App(f, x), App(g, y)) => alpha_eq(f, g) && alpha_eq(x, y),
        _ => false,
    }
}

pub fn free_vars(t: &Term) -> BTreeSet<String> {
    match t {
        Var(_) => BTreeSet::new(),
        Free(x) => BTreeSet::from([x.clone()]),
        Lam(_, b) => free_vars(b),
        App(f, a) => &free_vars(f) | &free_vars(a),
    }
}

pub fn size(t: &Term) -> usize {
    match t {
        Var(_) | Free(_) => 1,
        Lam(_, b) => 1 + size(b),
        App(f, a) => 1 + size(f) + size(a),
    }
}

// ---- parsing: term := \x y. term | atom+ ; atom := name | ( term ) ------

pub fn parse(src: &str) -> Result<Term, String> {
    parse_with(src, &[])
}

/// Free names listed in `defs` are replaced by their (closed) terms.
pub fn parse_with(src: &str, defs: &[(&str, Term)]) -> Result<Term, String> {
    let toks = tokens(src)?;
    let mut p = P { toks, pos: 0, scope: vec![], defs };
    let t = p.term()?;
    match p.toks.get(p.pos) {
        None => Ok(t),
        Some(x) => Err(format!("unexpected '{x}'")),
    }
}

fn tokens(src: &str) -> Result<Vec<String>, String> {
    let mut out = vec![];
    let cs: Vec<char> = src.chars().collect();
    let mut i = 0;
    while i < cs.len() {
        let c = cs[i];
        if c.is_whitespace() {
            i += 1;
        } else if "\\.()".contains(c) {
            out.push(c.to_string());
            i += 1;
        } else if c.is_alphanumeric() || c == '_' {
            let start = i;
            while i < cs.len() && (cs[i].is_alphanumeric() || cs[i] == '_' || cs[i] == '\'') {
                i += 1;
            }
            out.push(cs[start..i].iter().collect());
        } else {
            return Err(format!("unexpected character '{c}'"));
        }
    }
    Ok(out)
}

struct P<'a> {
    toks: Vec<String>,
    pos: usize,
    scope: Vec<String>, // binders, innermost last
    defs: &'a [(&'a str, Term)],
}

impl P<'_> {
    fn peek(&self) -> Option<&str> {
        self.toks.get(self.pos).map(|s| s.as_str())
    }
    fn term(&mut self) -> Result<Term, String> {
        if self.peek() == Some("\\") {
            self.pos += 1;
            let mut names = vec![];
            while let Some(x) = self.peek().filter(|x| *x != ".") {
                names.push(x.to_string());
                self.pos += 1;
            }
            if names.is_empty() || self.peek() != Some(".") {
                return Err("expected names and '.' after '\\'".into());
            }
            self.pos += 1;
            self.scope.extend(names.iter().cloned());
            let mut body = self.term()?;
            for x in names.iter().rev() {
                self.scope.pop();
                body = lam(x, body);
            }
            return Ok(body);
        }
        let mut t = self.atom()?;
        while let Some(x) = self.peek() {
            if x == ")" {
                break;
            }
            let a = if x == "\\" { self.term()? } else { self.atom()? };
            t = app(t, a);
        }
        Ok(t)
    }
    fn atom(&mut self) -> Result<Term, String> {
        match self.peek() {
            Some("(") => {
                self.pos += 1;
                let t = self.term()?;
                if self.peek() != Some(")") {
                    return Err("expected ')'".into());
                }
                self.pos += 1;
                Ok(t)
            }
            Some(x) if x != "." && x != ")" => {
                let x = x.to_string();
                self.pos += 1;
                if let Some(k) = self.scope.iter().rev().position(|y| *y == x) {
                    return Ok(Var(k));
                }
                Ok(match self.defs.iter().find(|(n, _)| *n == x) {
                    Some((_, t)) => t.clone(),
                    None => Free(x),
                })
            }
            other => Err(format!("unexpected {}", other.map_or("end".into(), |x| format!("'{x}'")))),
        }
    }
}

// ---- printing: names chosen fresh against the binders in scope ----------

pub fn show(t: &Term) -> String {
    let free = free_vars(t);
    let mut names = vec![];
    pr(t, &mut names, &free)
}

fn pr(t: &Term, names: &mut Vec<String>, free: &BTreeSet<String>) -> String {
    match t {
        Var(k) => names[names.len() - 1 - k].clone(),
        Free(x) => x.clone(),
        Lam(hint, b) => {
            let mut x = hint.clone();
            while names.contains(&x) || free.contains(&x) {
                x.push('\'');
            }
            names.push(x.clone());
            let body = pr(b, names, free);
            names.pop();
            format!("\\{x}. {body}")
        }
        App(f, a) => {
            let fs = match **f {
                Lam(..) => format!("({})", pr(f, names, free)),
                _ => pr(f, names, free),
            };
            let as_ = match **a {
                Lam(..) | App(..) => format!("({})", pr(a, names, free)),
                _ => pr(a, names, free),
            };
            format!("{fs} {as_}")
        }
    }
}
