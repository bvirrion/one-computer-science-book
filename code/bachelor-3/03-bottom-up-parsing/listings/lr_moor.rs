// lr_moor.rs -- Moor's expressions parsed by the generated tables, each
// tree compared with the one the hand-written parser of chapter 2 builds.
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "../../02-top-down-parsing/listings/ast.rs"]
mod ast;
#[path = "../../02-top-down-parsing/listings/parser.rs"]
mod parser;
#[path = "moor_expr_tables.rs"]
mod tables;
use tables::*;
use token::TokenKind as T;

/// The terminal of the grammar that a token stands for, and its text.
fn terminal(k: &T) -> (&'static str, String) {
    match k {
        T::Ident(x) => ("name", x.clone()),
        T::Number(v) => ("num", v.to_string()),
        T::True => ("true", "true".into()),
        T::False => ("false", "false".into()),
        T::Eof => ("$", String::new()),
        _ => {
            let s = parser::spell(k);
            let s = s.trim_matches('\'');
            let t = TERMINALS.iter().find(|t| **t == s).copied().unwrap_or("?");
            (t, String::new())
        }
    }
}

/// What a reduction builds from the values of the right side: the tree as an
/// S-expression, written as chapter 2's Display writes it.
fn build(rhs: &[&str], v: Vec<String>) -> String {
    match rhs {
        [_] => v[0].clone(),                                   // a chain, or a leaf
        ["-", _] => format!("(neg {})", v[1]),
        ["!", _] => format!("(! {})", v[1]),
        ["(", _, ")"] => v[1].clone(),
        ["name", "(", ")"] => format!("(call {})", v[0]),
        ["name", "(", _, ")"] => format!("(call {} {})", v[0], v[2]),
        ["name", "[", _, "]"] => format!("(index {} {})", v[0], v[2]),
        ["Args", ",", _] => format!("{} {}", v[0], v[2]),
        [_, op, _] => format!("({op} {} {})", v[0], v[2]),
        _ => unreachable!(),
    }
}

fn parse(src: &str) -> Result<String, String> {
    let toks = lexer::lex(src).map_err(|e| e.msg)?;
    let (mut states, mut values, mut i) = (vec![0usize], Vec::<String>::new(), 0);
    loop {
        let (term, text) = terminal(&toks[i].kind);
        let col = TERMINALS.iter().position(|t| *t == term).ok_or("not an expression token")?;
        let act = ACTION[*states.last().unwrap()][col];
        if act == ACCEPT {
            return Ok(values.pop().unwrap());
        } else if act > 0 {
            states.push(act as usize - 1);
            values.push(text);
            i += 1;
        } else if act < 0 {
            let (lhs, rhs) = RULES[(-act - 1) as usize];
            let v = values.split_off(values.len() - rhs.len());
            states.truncate(states.len() - rhs.len());
            values.push(build(rhs, v));
            let nt = NONTERMS.iter().position(|n| *n == lhs).unwrap();
            states.push(GOTO[*states.last().unwrap()][nt] as usize);
        } else {
            let (kind, col) = (&toks[i].kind, toks[i].span.col);
            return Err(format!("unexpected {} at column {col}", parser::spell(kind)));
        }
    }
}

fn main() {
    for src in ["1 - 2 - 3 * 4", "-x * y % 2", "!p && q || r", "a < b == c < d",
                "f(x, g(y) + 1, a[i - 1])", "(1 + 2) * 3", "a + * b"] {
        let lr = parse(src).unwrap_or_else(|e| format!("error: {e}"));
        let rd = parser::parse_expr(src).map(|e| e.to_string()).unwrap_or_else(|_| "error".into());
        let same = if lr == rd || lr.starts_with("error") && rd == "error" { "same" } else { "DIFFERENT" };
        println!("{src:<26} {lr}  [{same}]");
    }
}
