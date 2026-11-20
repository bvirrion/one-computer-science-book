// lam.rs -- the lambda-language of chapters 5 and 6 (files .lam): syntax tree,
// parser and printer. Frozen for the book.
#![allow(dead_code)]

/// Types, written only where a program annotates a lambda (chapter 6).
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Ty { Int, Bool, Fun(Box<Ty>, Box<Ty>), Pair(Box<Ty>, Box<Ty>), Var(u32) }

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Op { Add, Sub, Mul, Eq, Lt }

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum E {
    Int(i64),
    Bool(bool),
    Var(String),
    Lam(String, Option<Ty>, Box<E>),
    App(Box<E>, Box<E>),
    Let(String, Box<E>, Box<E>),
    LetRec(String, Box<E>, Box<E>), // letrec f = \x. e1 in e2
    Op(Op, Box<E>, Box<E>),
    If(Box<E>, Box<E>, Box<E>),
    Pair(Box<E>, Box<E>),
    Fst(Box<E>),
    Snd(Box<E>),
}

pub fn b(e: E) -> Box<E> {
    Box::new(e)
}

impl Op {
    pub fn symbol(self) -> &'static str {
        match self { Op::Add => "+", Op::Sub => "-", Op::Mul => "*", Op::Eq => "==", Op::Lt => "<" }
    }
}

// ---- lexer and parser ------------------------------------------------------

const KEYWORDS: [&str; 11] = ["let", "letrec", "in", "if", "then", "else", "true", "false", "fst", "snd", "int"];

fn tokens(src: &str) -> Result<Vec<String>, String> {
    let mut out = vec![];
    let cs: Vec<char> = src.chars().collect();
    let mut i = 0;
    while i < cs.len() {
        let c = cs[i];
        if c == '#' {
            while i < cs.len() && cs[i] != '\n' {
                i += 1;
            }
        } else if c.is_whitespace() {
            i += 1;
        } else if c.is_alphanumeric() || c == '_' {
            let s = i;
            while i < cs.len() && (cs[i].is_alphanumeric() || cs[i] == '_' || cs[i] == '\'') {
                i += 1;
            }
            out.push(cs[s..i].iter().collect());
        } else if i + 1 < cs.len() && ["==", "->"].contains(&&*format!("{c}{}", cs[i + 1])) {
            out.push(format!("{c}{}", cs[i + 1]));
            i += 2;
        } else if "\\.()=,+-*<:".contains(c) {
            out.push(c.to_string());
            i += 1;
        } else {
            return Err(format!("unexpected character '{c}'"));
        }
    }
    Ok(out)
}

pub fn parse(src: &str) -> Result<E, String> {
    let mut p = P { t: tokens(src)?, i: 0 };
    let e = p.expr()?;
    match p.t.get(p.i) {
        None => Ok(e),
        Some(x) => Err(format!("unexpected '{x}' after the expression")),
    }
}

struct P {
    t: Vec<String>,
    i: usize,
}

impl P {
    fn peek(&self) -> &str {
        self.t.get(self.i).map_or("", |s| s.as_str())
    }
    fn eat(&mut self, s: &str) -> Result<(), String> {
        if self.peek() == s {
            self.i += 1;
            return Ok(());
        }
        Err(format!("expected '{s}', found {}", if self.peek().is_empty() { "the end" } else { self.peek() }))
    }
    fn name(&mut self) -> Result<String, String> {
        let x = self.peek().to_string();
        if x.chars().next().is_some_and(|c| c.is_alphabetic() || c == '_') && !KEYWORDS.contains(&&*x) {
            self.i += 1;
            return Ok(x);
        }
        Err(format!("expected a name, found '{x}'"))
    }
    /// expr := \x[: T]. expr | let x = expr in expr | letrec f = expr in expr
    ///       | if expr then expr else expr | cmp
    fn expr(&mut self) -> Result<E, String> {
        match self.peek() {
            "\\" => {
                self.i += 1;
                let x = self.name()?;
                let ty = if self.peek() == ":" { self.i += 1; Some(self.ty()?) } else { None };
                self.eat(".")?;
                Ok(E::Lam(x, ty, b(self.expr()?)))
            }
            "let" | "letrec" => {
                let rec = self.peek() == "letrec";
                self.i += 1;
                let x = self.name()?;
                self.eat("=")?;
                let e1 = self.expr()?;
                self.eat("in")?;
                let e2 = self.expr()?;
                if rec && !matches!(e1, E::Lam(..)) {
                    return Err(format!("letrec {x} must be bound to a function"));
                }
                Ok(if rec { E::LetRec(x, b(e1), b(e2)) } else { E::Let(x, b(e1), b(e2)) })
            }
            "if" => {
                self.i += 1;
                let c = self.expr()?;
                self.eat("then")?;
                let t = self.expr()?;
                self.eat("else")?;
                Ok(E::If(b(c), b(t), b(self.expr()?)))
            }
            _ => self.cmp(),
        }
    }
    fn cmp(&mut self) -> Result<E, String> {
        let a = self.sum()?;
        let op = match self.peek() { "==" => Op::Eq, "<" => Op::Lt, _ => return Ok(a) };
        self.i += 1;
        Ok(E::Op(op, b(a), b(self.sum()?)))
    }
    fn sum(&mut self) -> Result<E, String> {
        let mut a = self.prod()?;
        while let Some(op) = match self.peek() { "+" => Some(Op::Add), "-" => Some(Op::Sub), _ => None } {
            self.i += 1;
            a = E::Op(op, b(a), b(self.prod()?));
        }
        Ok(a)
    }
    fn prod(&mut self) -> Result<E, String> {
        let mut a = self.app()?;
        while self.peek() == "*" {
            self.i += 1;
            a = E::Op(Op::Mul, b(a), b(self.app()?));
        }
        Ok(a)
    }
    /// Application by juxtaposition, to the left; a lambda, let or if may end it.
    fn app(&mut self) -> Result<E, String> {
        let mut f = self.atom()?;
        loop {
            let p = self.peek();
            if p == "\\" || p == "let" || p == "letrec" || p == "if" {
                return Ok(E::App(b(f), b(self.expr()?)));
            }
            if !(p == "(" || p == "fst" || p == "snd" || p == "true" || p == "false"
                 || p.chars().next().is_some_and(|c| c.is_alphanumeric() || c == '_') && !KEYWORDS.contains(&p)) {
                return Ok(f);
            }
            f = E::App(b(f), b(self.atom()?));
        }
    }
    fn atom(&mut self) -> Result<E, String> {
        let p = self.peek().to_string();
        match p.as_str() {
            "(" => {
                self.i += 1;
                let e = self.expr()?;
                if self.peek() == "," {
                    self.i += 1;
                    let e2 = self.expr()?;
                    self.eat(")")?;
                    return Ok(E::Pair(b(e), b(e2)));
                }
                self.eat(")")?;
                Ok(e)
            }
            "true" | "false" => {
                self.i += 1;
                Ok(E::Bool(p == "true"))
            }
            "fst" | "snd" => {
                self.i += 1;
                let a = self.atom()?;
                Ok(if p == "fst" { E::Fst(b(a)) } else { E::Snd(b(a)) })
            }
            _ if p.chars().next().is_some_and(|c| c.is_ascii_digit()) => {
                self.i += 1;
                p.parse().map(E::Int).map_err(|_| format!("bad number '{p}'"))
            }
            _ => Ok(E::Var(self.name()?)),
        }
    }
    fn ty(&mut self) -> Result<Ty, String> {
        let mut t = self.ty_atom()?;
        while self.peek() == "*" {
            self.i += 1;
            t = Ty::Pair(Box::new(t), Box::new(self.ty_atom()?));
        }
        if self.peek() == "->" {
            self.i += 1;
            return Ok(Ty::Fun(Box::new(t), Box::new(self.ty()?)));
        }
        Ok(t)
    }
    fn ty_atom(&mut self) -> Result<Ty, String> {
        match self.peek() {
            "int" => { self.i += 1; Ok(Ty::Int) }
            "bool" => { self.i += 1; Ok(Ty::Bool) }
            "(" => {
                self.i += 1;
                let t = self.ty()?;
                self.eat(")")?;
                Ok(t)
            }
            other => Err(format!("expected a type, found '{other}'")),
        }
    }
}

// ---- printer ---------------------------------------------------------------

/// Parenthesised as needed: levels 0 (lambda, let, if), 1 (comparison), 2 (sum),
/// 3 (product), 4 (application), 5 (atom).
pub fn show(e: &E) -> String {
    pr(e, 0)
}

fn level(e: &E) -> u8 {
    match e {
        E::Lam(..) | E::Let(..) | E::LetRec(..) | E::If(..) => 0,
        E::Op(Op::Eq | Op::Lt, ..) => 1,
        E::Op(Op::Add | Op::Sub, ..) => 2,
        E::Op(Op::Mul, ..) => 3,
        E::App(..) | E::Fst(_) | E::Snd(_) => 4,
        _ => 5,
    }
}

fn pr(e: &E, min: u8) -> String {
    let s = match e {
        E::Int(n) => n.to_string(),
        E::Bool(v) => v.to_string(),
        E::Var(x) => x.clone(),
        E::Lam(x, Some(t), body) => format!("\\{x}: {}. {}", show_ty(t), pr(body, 0)),
        E::Lam(x, None, body) => format!("\\{x}. {}", pr(body, 0)),
        E::App(f, a) => format!("{} {}", pr(f, 4), pr(a, 5)),
        E::Let(x, a, body) => format!("let {x} = {} in {}", pr(a, 0), pr(body, 0)),
        E::LetRec(x, a, body) => format!("letrec {x} = {} in {}", pr(a, 0), pr(body, 0)),
        E::Op(op, a, c) => {
            let l = level(e);
            let (la, lc) = if l == 1 { (2, 2) } else { (l, l + 1) };
            format!("{} {} {}", pr(a, la), op.symbol(), pr(c, lc))
        }
        E::If(c, t, f) => format!("if {} then {} else {}", pr(c, 0), pr(t, 0), pr(f, 0)),
        E::Pair(a, c) => format!("({}, {})", pr(a, 0), pr(c, 0)),
        E::Fst(a) => format!("fst {}", pr(a, 5)),
        E::Snd(a) => format!("snd {}", pr(a, 5)),
    };
    if level(e) < min { format!("({s})") } else { s }
}

pub fn show_ty(t: &Ty) -> String {
    match t {
        Ty::Int => "int".into(),
        Ty::Bool => "bool".into(),
        Ty::Var(k) => format!("'{}", (b'a' + (*k % 26) as u8) as char) + &"'".repeat((*k / 26) as usize),
        Ty::Pair(a, c) => format!("{} * {}", ty_paren(a, true), ty_paren(c, true)),
        Ty::Fun(a, c) => format!("{} -> {}", ty_paren(a, false), show_ty(c)),
    }
}

fn ty_paren(t: &Ty, in_pair: bool) -> String {
    match t {
        Ty::Fun(..) => format!("({})", show_ty(t)),
        Ty::Pair(..) if in_pair => format!("({})", show_ty(t)),
        _ => show_ty(t),
    }
}
