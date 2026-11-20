// pb_fines.rs -- the weekend problem: the library's fines formulas, parsed
// by recursive descent (one function per level) and by precedence
// climbing, with the calls of each counted.
#![allow(dead_code)]

#[derive(Debug, PartialEq, Clone)]
pub enum Tree {
    Num(i64),
    Name(String),
    Call(String, Vec<Tree>),
    Op(String, Box<Tree>, Box<Tree>),
}

/// The operator levels, loosest first; `^` (the last) is right-associative.
pub const LEVELS: [&[&str]; 7] =
    [&["or"], &["and"], &["==", "!="], &["<", "<=", ">", ">="], &["+", "-"], &["*", "/"], &["^"]];

pub fn tokens(s: &str) -> Vec<String> {
    let mut out = Vec::new();
    let b = s.as_bytes();
    let mut i = 0;
    while i < b.len() {
        let c = b[i];
        let start = i;
        if c.is_ascii_whitespace() {
            i += 1;
            continue;
        } else if c.is_ascii_alphanumeric() {
            while i < b.len() && (b[i].is_ascii_alphanumeric() || b[i] == b'_') {
                i += 1;
            }
        } else if i + 1 < b.len() && ["<=", ">=", "==", "!="].contains(&&s[i..i + 2]) {
            i += 2;
        } else {
            i += 1;
        }
        out.push(s[start..i].to_string());
    }
    out.push("$".into());
    out
}

fn level_of(t: &str) -> Option<usize> {
    LEVELS.iter().position(|ops| ops.contains(&t))
}

pub struct Rd<'a> {
    toks: &'a [String],
    pos: usize,
    pub calls: usize,
}

impl<'a> Rd<'a> {
    pub fn new(toks: &'a [String]) -> Self {
        Rd { toks, pos: 0, calls: 0 }
    }
    fn peek(&self) -> &str {
        &self.toks[self.pos]
    }
    /// One function per level: level k parses operands of level k + 1.
    pub fn level(&mut self, k: usize) -> Tree {
        self.calls += 1;
        if k == LEVELS.len() {
            return self.primary();
        }
        let mut lhs = self.level(k + 1);
        while LEVELS[k].contains(&self.peek()) {
            let op = self.peek().to_string();
            self.pos += 1;
            let rhs = if k == LEVELS.len() - 1 { self.level(k) } else { self.level(k + 1) };
            lhs = Tree::Op(op, Box::new(lhs), Box::new(rhs));
            if k == LEVELS.len() - 1 {
                break; // right-associative: the recursion took the rest
            }
        }
        lhs
    }
    fn primary(&mut self) -> Tree {
        let t = self.peek().to_string();
        self.pos += 1;
        if t == "(" {
            let e = self.level(0);
            self.pos += 1; // )
            return e;
        }
        if let Ok(v) = t.parse() {
            return Tree::Num(v);
        }
        if self.peek() == "(" {
            self.pos += 1;
            let mut args = vec![self.level(0)];
            while self.peek() == "," {
                self.pos += 1;
                args.push(self.level(0));
            }
            self.pos += 1;
            return Tree::Call(t, args);
        }
        Tree::Name(t)
    }
}

pub struct Pc<'a> {
    toks: &'a [String],
    pos: usize,
    pub calls: usize,
}

impl<'a> Pc<'a> {
    pub fn new(toks: &'a [String]) -> Self {
        Pc { toks, pos: 0, calls: 0 }
    }
    fn peek(&self) -> &str {
        &self.toks[self.pos]
    }
    /// Precedence climbing: binding power = level + 1.
    pub fn expr(&mut self, min: usize) -> Tree {
        self.calls += 1;
        let mut lhs = self.primary();
        while let Some(k) = level_of(self.peek()) {
            let bp = k + 1;
            if bp < min {
                break;
            }
            let op = self.peek().to_string();
            self.pos += 1;
            let right_assoc = k == LEVELS.len() - 1;
            let rhs = self.expr(if right_assoc { bp } else { bp + 1 });
            lhs = Tree::Op(op, Box::new(lhs), Box::new(rhs));
        }
        lhs
    }
    fn primary(&mut self) -> Tree {
        self.calls += 1;
        let t = self.peek().to_string();
        self.pos += 1;
        if t == "(" {
            let e = self.expr(1);
            self.pos += 1;
            return e;
        }
        if let Ok(v) = t.parse() {
            return Tree::Num(v);
        }
        if self.peek() == "(" {
            self.pos += 1;
            let mut args = vec![self.expr(1)];
            while self.peek() == "," {
                self.pos += 1;
                args.push(self.expr(1));
            }
            self.pos += 1;
            return Tree::Call(t, args);
        }
        Tree::Name(t)
    }
}

pub fn eval(t: &Tree, env: &dyn Fn(&str) -> i64) -> i64 {
    match t {
        Tree::Num(v) => *v,
        Tree::Name(x) => env(x),
        Tree::Call(f, args) => {
            let v: Vec<i64> = args.iter().map(|a| eval(a, env)).collect();
            match f.as_str() {
                "max" => *v.iter().max().unwrap(),
                "min" => *v.iter().min().unwrap(),
                _ => panic!("unknown function {f}"),
            }
        }
        Tree::Op(op, a, b) => {
            let (x, y) = (eval(a, env), eval(b, env));
            match op.as_str() {
                "+" => x + y, "-" => x - y, "*" => x * y, "/" => x / y, "^" => x.pow(y as u32),
                "<" => (x < y) as i64, "<=" => (x <= y) as i64, ">" => (x > y) as i64,
                ">=" => (x >= y) as i64, "==" => (x == y) as i64, "!=" => (x != y) as i64,
                "and" => (x != 0 && y != 0) as i64, "or" => (x != 0 || y != 0) as i64,
                _ => panic!("unknown operator {op}"),
            }
        }
    }
}

/// Parse with both methods: the trees, and the calls each made.
pub fn both(src: &str) -> (Tree, usize, Tree, usize) {
    let t = tokens(src);
    let mut rd = Rd::new(&t);
    let a = rd.level(0);
    let mut pc = Pc::new(&t);
    let b = pc.expr(1);
    (a, rd.calls, b, pc.calls)
}
