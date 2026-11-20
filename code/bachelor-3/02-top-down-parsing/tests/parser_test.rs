// Tests of the parser (listings/parser.rs) and the AST printer.
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "../listings/ast.rs"]
mod ast;
#[path = "../listings/parser.rs"]
mod parser;

fn tree(src: &str) -> String {
    parser::parse_expr(src).unwrap().to_string()
}

#[test]
fn precedence_and_associativity() {
    assert_eq!(tree("1 - 2 - 3 * 4"), "(- (- 1 2) (* 3 4))");
    assert_eq!(tree("a || b && c == d < e + f * g"), "(|| a (&& b (== c (< d (+ e (* f g))))))");
    assert_eq!(tree("a * b + c * d"), "(+ (* a b) (* c d))");
    assert_eq!(tree("8 / 4 / 2 % 3"), "(% (/ (/ 8 4) 2) 3)");
    assert_eq!(tree("- - x"), "(neg (neg x))");
    assert_eq!(tree("(a + b) * c"), "(* (+ a b) c)");
    assert_eq!(tree("f(x, g(1), a[i + 1])"), "(call f x (call g 1) (index a (+ i 1)))");
    assert_eq!(tree("a - -b * c % d || !e"), "(|| (- a (% (* (neg b) c) d)) (! e))"); // exercise 2
}

/// Every binary node's operator binds no tighter than its children's, and
/// a left-associative operator never has an equal one as right child.
fn check(e: &ast::Expr) -> u8 {
    use ast::ExprKind::*;
    let bp = |op: ast::BinOp| match op.symbol() {
        "||" => 1, "&&" => 2, "==" | "!=" => 3, "<" | "<=" | ">" | ">=" => 4, "+" | "-" => 5, _ => 6,
    };
    match &e.kind {
        Binary(op, a, b) => {
            let (l, r, me) = (check(a), check(b), bp(*op));
            assert!(l >= me && r > me, "bad tree {e}");
            me
        }
        Unary(_, a) => {
            check(a);
            9
        }
        _ => 10,
    }
}

#[test]
fn trees_of_generated_expressions_respect_the_table() {
    let ops = ["||", "&&", "==", "!=", "<", "<=", "+", "-", "*", "/", "%"];
    let mut seed: u64 = 3;
    for _ in 0..3000 {
        let mut s = String::from("x0");
        for i in 1..9 {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            s += &format!(" {} x{}", ops[(seed >> 33) as usize % ops.len()], i);
        }
        check(&parser::parse_expr(&s).unwrap());
    }
}

#[test]
fn fib_parses_and_prints() {
    let src = std::fs::read_to_string("../listings/fib.moor").unwrap();
    let p = parser::parse_source(&src, "fib.moor").unwrap();
    assert_eq!(p.items.len(), 2);
    let text = ast::pretty(&p);
    assert!(text.contains("return (+ (call fib (- n 1)) (call fib (- n 2)))"));
}

#[test]
fn statements() {
    let p = parser::parse_source(
        "var g: int = -3; array a[10]; fn f(x: int, b: bool) -> bool { a[x] = 1; x = 2; if b { } else if x < 1 { return true; } else { f(1, b); } { var y: int = x; } while b { return false; } return b; }",
        "t.moor").unwrap();
    let text = ast::pretty(&p);
    assert!(text.starts_with("global g: int = -3\narray a[10]\nfn f(x: int, b: bool) -> bool\n"));
    assert!(text.contains("  a[x] = 1\n  x = 2\n  if b\n  else\n    if (< x 1)\n      return true\n    else\n      (call f 1 b)\n"));
    assert!(text.contains("  block\n    var y: int = x\n  while b\n    return false\n  return b\n"));
}

#[test]
fn errors_are_reported_with_recovery() {
    let src = std::fs::read_to_string("../listings/errors.moor").unwrap();
    let toks = lexer::lex(&src).unwrap();
    let mut p = parser::Parser::new(&toks);
    p.program();
    let got: Vec<(u32, u32, &str)> = p.errors.iter().map(|e| (e.span.line, e.span.col, e.msg.as_str())).collect();
    assert_eq!(got, vec![
        (2, 19, "expected ')', found ';'"),
        (3, 13, "expected an expression, found ';'"),
        (4, 25, "expected ';', found '}'"),
    ]);
}

#[test]
fn exercise_8_messages() {
    let src = std::fs::read_to_string("../exercises/ex8.moor").unwrap();
    let toks = lexer::lex(&src).unwrap();
    let mut p = parser::Parser::new(&toks);
    p.program();
    let got: Vec<(u32, u32, &str)> = p.errors.iter().map(|e| (e.span.line, e.span.col, e.msg.as_str())).collect();
    assert_eq!(got, vec![
        (2, 16, "expected an expression, found '*'"),
        (4, 5, "expected ';', found name 'print'"),
        (6, 1, "expected '}', found end of file"),
    ]);
}

#[test]
fn assignment_targets() {
    assert!(parser::parse_source("fn main() { f(x) = 1; }", "t").unwrap_err().contains("only a name or an array element"));
    assert!(parser::parse_source("fn main() { (x) = 1; }", "t").is_err());
    assert!(parser::parse_expr("f(x)[2]").is_err());
}
