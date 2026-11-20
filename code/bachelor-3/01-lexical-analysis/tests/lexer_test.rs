// Tests of the hand-written scanner (listings/lexer.rs).
#[path = "../listings/lexer.rs"]
mod lexer;
#[path = "../listings/token.rs"]
mod token;
use token::TokenKind::{self, *};

fn kinds(src: &str) -> Vec<TokenKind> {
    lexer::lex(src).unwrap().into_iter().map(|t| t.kind).collect()
}

#[test]
fn keywords_are_not_identifiers() {
    assert_eq!(kinds("if iffy _if if2"), vec![If, Ident("iffy".into()), Ident("_if".into()), Ident("if2".into()), Eof]);
}

#[test]
fn longest_operator_wins() {
    assert_eq!(kinds("<= < = == -> - >"), vec![Le, Lt, Assign, EqEq, Arrow, Minus, Gt, Eof]);
    assert_eq!(kinds("a<=-b"), vec![Ident("a".into()), Le, Minus, Ident("b".into()), Eof]);
}

#[test]
fn comments_and_spaces_vanish() {
    assert_eq!(kinds("x // y z\n\t1//"), vec![Ident("x".into()), Number(1), Eof]);
}

#[test]
fn spans_give_line_and_column() {
    let toks = lexer::lex("fn f() {\n\treturn 12;\n}").unwrap();
    let r = &toks[5];
    assert_eq!(r.kind, Return);
    assert_eq!((r.span.line, r.span.col, r.span.start, r.span.end), (2, 2, 10, 16));
    let n = &toks[6];
    assert_eq!((n.span.line, n.span.col, n.span.end - n.span.start), (2, 9, 2));
}

#[test]
fn numbers_must_fit_32_bits() {
    assert_eq!(kinds("2147483647"), vec![Number(2147483647), Eof]);
    let e = lexer::lex("2147483648").unwrap_err();
    assert_eq!(e.msg, "number too large");
}

#[test]
fn errors_and_recovery() {
    let src = std::fs::read_to_string("../listings/bad.moor").unwrap();
    let (toks, errs) = lexer::lex_recover(&src);
    assert_eq!(errs.len(), 3);
    assert_eq!((errs[0].span.line, errs[0].span.col), (2, 12));
    assert_eq!((errs[1].span.line, errs[1].span.col), (3, 14));
    assert_eq!((errs[2].span.line, errs[2].span.col), (4, 12));
    assert_eq!(toks.last().unwrap().kind, Eof);
    let shown = lexer::show_error(&src, "bad.moor", &errs[0]);
    assert!(shown.ends_with("\t          ^\n"));
}

#[test]
fn hello_has_the_expected_stream() {
    let src = std::fs::read_to_string("../listings/hello.moor").unwrap();
    let toks = lexer::lex(&src).unwrap();
    assert_eq!(toks.len(), 49);
    assert!(toks.iter().all(|t| &src[t.span.start..t.span.end] != " "));
}
