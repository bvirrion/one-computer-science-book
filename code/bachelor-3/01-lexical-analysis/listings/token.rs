// token.rs -- the tokens of Moor and where they come from in the source.
// Frozen for the book: every later chapter includes this file unchanged.
#![allow(dead_code)]

/// A stretch of the source: byte offsets `start..end`, and the line and
/// column (both from 1) of its first character.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Span {
    pub start: usize,
    pub end: usize,
    pub line: u32,
    pub col: u32,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum TokenKind {
    // keywords
    Fn, Var, Array, If, Else, While, Return, True, False, Int, Bool,
    // names and literals
    Ident(String),
    Number(i64),
    // operators
    Plus, Minus, Star, Slash, Percent,
    EqEq, NotEq, Lt, Le, Gt, Ge,
    AndAnd, OrOr, Bang, Assign,
    // punctuation
    LParen, RParen, LBrace, RBrace, LBracket, RBracket,
    Comma, Semi, Colon, Arrow,
    Eof,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Token {
    pub kind: TokenKind,
    pub span: Span,
}

/// The keyword spelled `word`, if it is one.
pub fn keyword(word: &str) -> Option<TokenKind> {
    use TokenKind::*;
    Some(match word {
        "fn" => Fn, "var" => Var, "array" => Array, "if" => If,
        "else" => Else, "while" => While, "return" => Return,
        "true" => True, "false" => False, "int" => Int, "bool" => Bool,
        _ => return None,
    })
}

/// The token class, as the scanner tables and the messages name it.
pub fn class_name(kind: &TokenKind) -> &'static str {
    use TokenKind::*;
    match kind {
        Ident(_) => "ident",
        Number(_) => "number",
        Fn | Var | Array | If | Else | While | Return | True | False | Int | Bool => "keyword",
        Eof => "eof",
        _ => "symbol",
    }
}
