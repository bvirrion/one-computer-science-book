// lexer.rs -- the hand-written scanner of Moor. Frozen for the book.
#![allow(dead_code)]
use crate::token::{keyword, Span, Token, TokenKind};

#[derive(Debug, PartialEq, Eq)]
pub struct LexError {
    pub msg: String,
    pub span: Span,
}

pub struct Lexer<'a> {
    src: &'a [u8],
    pos: usize, // byte offset of the next character
    line: u32,
    col: u32, // a column counts characters, so a tab is one column
}

impl<'a> Lexer<'a> {
    pub fn new(src: &'a str) -> Self {
        Lexer { src: src.as_bytes(), pos: 0, line: 1, col: 1 }
    }

    fn peek(&self, k: usize) -> Option<u8> {
        self.src.get(self.pos + k).copied()
    }

    fn bump(&mut self) {
        let c = self.src[self.pos];
        self.pos += 1;
        if c == b'\n' {
            self.line += 1;
            self.col = 1;
        } else if c & 0xC0 != 0x80 {
            self.col += 1; // the continuation bytes of a UTF-8 character add nothing
        }
    }

    fn skip_trivia(&mut self) {
        loop {
            match self.peek(0) {
                Some(b' ' | b'\t' | b'\r' | b'\n') => self.bump(),
                Some(b'/') if self.peek(1) == Some(b'/') => {
                    while !matches!(self.peek(0), None | Some(b'\n')) {
                        self.bump();
                    }
                }
                _ => return,
            }
        }
    }

    /// The next token, or an error covering the offending character.
    pub fn next_token(&mut self) -> Result<Token, LexError> {
        self.skip_trivia();
        let (start, line, col) = (self.pos, self.line, self.col);
        let span = |end| Span { start, end, line, col };
        let Some(c) = self.peek(0) else {
            return Ok(Token { kind: TokenKind::Eof, span: span(start) });
        };
        let kind = if c.is_ascii_alphabetic() || c == b'_' {
            while matches!(self.peek(0), Some(d) if d.is_ascii_alphanumeric() || d == b'_') {
                self.bump();
            }
            let word = std::str::from_utf8(&self.src[start..self.pos]).unwrap();
            keyword(word).unwrap_or_else(|| TokenKind::Ident(word.to_string()))
        } else if c.is_ascii_digit() {
            while matches!(self.peek(0), Some(d) if d.is_ascii_digit()) {
                self.bump();
            }
            let text = std::str::from_utf8(&self.src[start..self.pos]).unwrap();
            match text.parse::<i64>() {
                Ok(v) if v <= i32::MAX as i64 => TokenKind::Number(v),
                _ => Err(LexError { msg: "number too large".into(), span: span(self.pos) })?,
            }
        } else {
            self.symbol(c).map_err(|msg| LexError { msg, span: span(self.pos) })?
        };
        Ok(Token { kind, span: span(self.pos) })
    }

    /// Operators and punctuation: two-character ones first (the longest match).
    fn symbol(&mut self, c: u8) -> Result<TokenKind, String> {
        use TokenKind::*;
        let two = match (c, self.peek(1)) {
            (b'=', Some(b'=')) => Some(EqEq),
            (b'!', Some(b'=')) => Some(NotEq),
            (b'<', Some(b'=')) => Some(Le),
            (b'>', Some(b'=')) => Some(Ge),
            (b'&', Some(b'&')) => Some(AndAnd),
            (b'|', Some(b'|')) => Some(OrOr),
            (b'-', Some(b'>')) => Some(Arrow),
            _ => None,
        };
        if let Some(k) = two {
            self.bump();
            self.bump();
            return Ok(k);
        }
        let one = match c {
            b'+' => Plus, b'-' => Minus, b'*' => Star, b'/' => Slash, b'%' => Percent,
            b'<' => Lt, b'>' => Gt, b'!' => Bang, b'=' => Assign,
            b'(' => LParen, b')' => RParen, b'{' => LBrace, b'}' => RBrace,
            b'[' => LBracket, b']' => RBracket, b',' => Comma, b';' => Semi, b':' => Colon,
            _ => {
                self.bump(); // skip the whole character, even a multi-byte one
                while matches!(self.peek(0), Some(d) if d & 0xC0 == 0x80) {
                    self.bump();
                }
                let s = String::from_utf8_lossy(&self.src[self.pos - self.char_len()..self.pos]);
                return Err(match c {
                    b'&' | b'|' => format!("expected '{0}{0}', found a single '{0}'", c as char),
                    _ => format!("unexpected character '{}'", s),
                });
            }
        };
        self.bump();
        Ok(one)
    }

    fn char_len(&self) -> usize {
        let mut k = 1;
        while self.src[self.pos - k] & 0xC0 == 0x80 {
            k += 1;
        }
        k
    }
}

/// The whole token stream, ending with Eof, or the first error.
pub fn lex(src: &str) -> Result<Vec<Token>, LexError> {
    let mut lx = Lexer::new(src);
    let mut out = Vec::new();
    loop {
        let t = lx.next_token()?;
        let end = t.kind == TokenKind::Eof;
        out.push(t);
        if end {
            return Ok(out);
        }
    }
}

/// Every token and every error: after an error the scanner has skipped the
/// offending character and goes on.
pub fn lex_recover(src: &str) -> (Vec<Token>, Vec<LexError>) {
    let mut lx = Lexer::new(src);
    let (mut toks, mut errs) = (Vec::new(), Vec::new());
    loop {
        match lx.next_token() {
            Ok(t) if t.kind == TokenKind::Eof => {
                toks.push(t);
                return (toks, errs);
            }
            Ok(t) => toks.push(t),
            Err(e) => errs.push(e),
        }
    }
}

/// The message under the source line, a caret under the column. Tabs before
/// the column are copied, so the caret lines up whatever the tab width.
pub fn show_error(src: &str, file: &str, e: &LexError) -> String {
    let text = src.lines().nth(e.span.line as usize - 1).unwrap_or("");
    let pad: String = text
        .chars()
        .take(e.span.col as usize - 1)
        .map(|c| if c == '\t' { '\t' } else { ' ' })
        .collect();
    format!("{}:{}:{}: error: {}\n  {}\n  {}^\n", file, e.span.line, e.span.col, e.msg, text, pad)
}
