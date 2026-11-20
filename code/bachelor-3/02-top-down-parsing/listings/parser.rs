// parser.rs -- the recursive-descent parser of Moor: one function per
// nonterminal, precedence climbing for expressions, panic-mode recovery.
// Frozen for the book.
#![allow(dead_code)]
use crate::ast::*;
use crate::token::{Span, Token, TokenKind as T};

#[derive(Debug, PartialEq)]
pub struct ParseError {
    pub msg: String,
    pub span: Span,
}

/// Err(()) means: an error has been recorded in `errors`.
type R<X> = Result<X, ()>;

pub struct Parser<'a> {
    toks: &'a [Token], // ends with Eof
    pos: usize,
    pub errors: Vec<ParseError>,
}

pub fn join(a: Span, b: Span) -> Span {
    Span { start: a.start, end: b.end, line: a.line, col: a.col }
}

/// How a token is named in an error message.
pub fn spell(k: &T) -> String {
    let s = match k {
        T::Ident(x) => return format!("name '{x}'"),
        T::Number(v) => return format!("number {v}"),
        T::Eof => return "end of file".into(),
        T::Fn => "fn", T::Var => "var", T::Array => "array", T::If => "if", T::Else => "else",
        T::While => "while", T::Return => "return", T::True => "true", T::False => "false",
        T::Int => "int", T::Bool => "bool", T::Plus => "+", T::Minus => "-", T::Star => "*",
        T::Slash => "/", T::Percent => "%", T::EqEq => "==", T::NotEq => "!=", T::Lt => "<",
        T::Le => "<=", T::Gt => ">", T::Ge => ">=", T::AndAnd => "&&", T::OrOr => "||",
        T::Bang => "!", T::Assign => "=", T::LParen => "(", T::RParen => ")", T::LBrace => "{",
        T::RBrace => "}", T::LBracket => "[", T::RBracket => "]", T::Comma => ",", T::Semi => ";",
        T::Colon => ":", T::Arrow => "->",
    };
    format!("'{s}'")
}

/// The binary operators: their tree node and binding power.
fn binop(k: &T) -> Option<(BinOp, u8)> {
    Some(match k {
        T::OrOr => (BinOp::Or, 1),
        T::AndAnd => (BinOp::And, 2),
        T::EqEq => (BinOp::Eq, 3),
        T::NotEq => (BinOp::Ne, 3),
        T::Lt => (BinOp::Lt, 4),
        T::Le => (BinOp::Le, 4),
        T::Gt => (BinOp::Gt, 4),
        T::Ge => (BinOp::Ge, 4),
        T::Plus => (BinOp::Add, 5),
        T::Minus => (BinOp::Sub, 5),
        T::Star => (BinOp::Mul, 6),
        T::Slash => (BinOp::Div, 6),
        T::Percent => (BinOp::Rem, 6),
        _ => return None,
    })
}

impl<'a> Parser<'a> {
    pub fn new(toks: &'a [Token]) -> Self {
        Parser { toks, pos: 0, errors: Vec::new() }
    }

    fn peek(&self) -> &T {
        &self.toks[self.pos].kind
    }
    fn peek2(&self) -> &T {
        &self.toks[(self.pos + 1).min(self.toks.len() - 1)].kind
    }
    fn span(&self) -> Span {
        self.toks[self.pos].span
    }
    fn prev(&self) -> Span {
        self.toks[self.pos.saturating_sub(1)].span
    }
    fn bump(&mut self) -> Span {
        let s = self.span();
        if self.pos + 1 < self.toks.len() {
            self.pos += 1;
        }
        s
    }
    fn error<X>(&mut self, msg: String) -> R<X> {
        let span = self.span();
        self.errors.push(ParseError { msg, span });
        Err(())
    }
    fn expect(&mut self, k: T, what: &str) -> R<Span> {
        if *self.peek() == k {
            return Ok(self.bump());
        }
        let found = spell(self.peek());
        self.error(format!("expected {what}, found {found}"))
    }
    fn ident(&mut self) -> R<(String, Span)> {
        if let T::Ident(x) = self.peek().clone() {
            return Ok((x, self.bump()));
        }
        let found = spell(self.peek());
        self.error(format!("expected a name, found {found}"))
    }

    // ---- items --------------------------------------------------------
    pub fn program(&mut self) -> Program {
        let mut items = Vec::new();
        while *self.peek() != T::Eof {
            match self.item() {
                Ok(it) => items.push(it),
                Err(()) => self.sync_item(),
            }
        }
        Program { items }
    }

    fn sync_item(&mut self) {
        while !matches!(self.peek(), T::Fn | T::Var | T::Array | T::Eof) {
            self.bump();
        }
    }

    fn item(&mut self) -> R<Item> {
        match self.peek() {
            T::Fn => self.func().map(Item::Func),
            T::Var => {
                let start = self.bump();
                let (name, _) = self.ident()?;
                self.expect(T::Colon, "':' and a type")?;
                let ty = self.ty()?;
                let init = if *self.peek() == T::Assign {
                    self.bump();
                    Some(self.literal()?)
                } else {
                    None
                };
                let end = self.expect(T::Semi, "';'")?;
                Ok(Item::Global { name, ty, init, span: join(start, end) })
            }
            T::Array => {
                let start = self.bump();
                let (name, _) = self.ident()?;
                self.expect(T::LBracket, "'['")?;
                let size = match *self.peek() {
                    T::Number(n) => n,
                    _ => return self.error("expected the array's size, a number".into()),
                };
                self.bump();
                self.expect(T::RBracket, "']'")?;
                let end = self.expect(T::Semi, "';'")?;
                Ok(Item::Array { name, size, span: join(start, end) })
            }
            k => {
                let found = spell(k);
                self.error(format!("expected 'fn', 'var' or 'array', found {found}"))
            }
        }
    }

    fn func(&mut self) -> R<Func> {
        let start = self.bump(); // fn
        let (name, _) = self.ident()?;
        self.expect(T::LParen, "'('")?;
        let mut params = Vec::new();
        while *self.peek() != T::RParen {
            let (pname, pspan) = self.ident()?;
            self.expect(T::Colon, "':' and a type")?;
            let ty = self.ty()?;
            params.push(Param { name: pname, ty, span: join(pspan, self.prev()) });
            if *self.peek() != T::Comma {
                break;
            }
            self.bump();
        }
        self.expect(T::RParen, "')'")?;
        let ret = if *self.peek() == T::Arrow {
            self.bump();
            Some(self.ty()?)
        } else {
            None
        };
        let body = self.block()?;
        Ok(Func { name, params, ret, span: join(start, body.span), body })
    }

    fn ty(&mut self) -> R<Type> {
        let t = match self.peek() {
            T::Int => Type::Int,
            T::Bool => Type::Bool,
            k => {
                let found = spell(k);
                return self.error(format!("expected a type, found {found}"));
            }
        };
        self.bump();
        Ok(t)
    }

    fn literal(&mut self) -> R<Expr> {
        let start = self.span();
        let kind = match self.peek().clone() {
            T::Number(v) => ExprKind::Int(v),
            T::True => ExprKind::Bool(true),
            T::False => ExprKind::Bool(false),
            T::Minus => match self.peek2().clone() {
                T::Number(v) => {
                    self.bump();
                    ExprKind::Int(-v)
                }
                _ => return self.error("expected a number after '-'".into()),
            },
            k => return self.error(format!("expected a literal, found {}", spell(&k))),
        };
        let end = self.bump();
        Ok(Expr { kind, span: join(start, end) })
    }

    // ---- statements ---------------------------------------------------
    fn block(&mut self) -> R<Block> {
        let start = self.expect(T::LBrace, "'{'")?;
        let mut stmts = Vec::new();
        while !matches!(self.peek(), T::RBrace | T::Eof | T::Fn) {
            match self.stmt() {
                Ok(s) => stmts.push(s),
                Err(()) => self.sync_stmt(),
            }
        }
        let end = self.expect(T::RBrace, "'}'")?;
        Ok(Block { stmts, span: join(start, end) })
    }

    /// Panic mode: skip to a synchronising token. A ';' is consumed; a
    /// token that starts a statement, a '}' or 'fn' is left for the caller.
    fn sync_stmt(&mut self) {
        loop {
            match self.peek() {
                T::Semi => {
                    self.bump();
                    return;
                }
                T::RBrace | T::Eof | T::Fn | T::Var | T::If | T::While | T::Return => return,
                _ => {
                    self.bump();
                }
            }
        }
    }

    fn stmt(&mut self) -> R<Stmt> {
        let start = self.span();
        let kind = match self.peek() {
            T::Var => {
                self.bump();
                let (name, _) = self.ident()?;
                let ty = if *self.peek() == T::Colon {
                    self.bump();
                    Some(self.ty()?)
                } else {
                    None
                };
                self.expect(T::Assign, "'='")?;
                let e = self.expr()?;
                self.expect(T::Semi, "';'")?;
                StmtKind::Var(name, ty, e)
            }
            T::If => return self.if_stmt(),
            T::While => {
                self.bump();
                let cond = self.expr()?;
                StmtKind::While(cond, self.block()?)
            }
            T::Return => {
                self.bump();
                let e = if *self.peek() == T::Semi { None } else { Some(self.expr()?) };
                self.expect(T::Semi, "';'")?;
                StmtKind::Return(e)
            }
            T::LBrace => StmtKind::Block(self.block()?),
            T::Ident(_) if *self.peek2() == T::Assign => {
                let (name, _) = self.ident()?;
                self.bump(); // =
                let e = self.expr()?;
                self.expect(T::Semi, "';'")?;
                StmtKind::Assign(name, e)
            }
            _ => {
                let e = self.expr()?;
                if *self.peek() == T::Assign {
                    let ExprKind::Index(a, i) = e.kind else {
                        return self.error("only a name or an array element can be assigned to".into());
                    };
                    self.bump();
                    let v = self.expr()?;
                    self.expect(T::Semi, "';'")?;
                    StmtKind::AssignIndex(a, *i, v)
                } else {
                    self.expect(T::Semi, "';'")?;
                    StmtKind::Expr(e)
                }
            }
        };
        Ok(Stmt { kind, span: join(start, self.prev()) })
    }

    fn if_stmt(&mut self) -> R<Stmt> {
        let start = self.bump(); // if
        let cond = self.expr()?;
        let then = self.block()?;
        let other = if *self.peek() == T::Else {
            self.bump();
            if *self.peek() == T::If {
                let s = self.if_stmt()?;
                Some(Block { span: s.span, stmts: vec![s] })
            } else {
                Some(self.block()?)
            }
        } else {
            None
        };
        Ok(Stmt { kind: StmtKind::If(cond, then, other), span: join(start, self.prev()) })
    }

    // ---- expressions: precedence climbing ------------------------------
    pub fn expr(&mut self) -> R<Expr> {
        self.expr_bp(1)
    }

    /// An expression whose operators all bind at least as tightly as `min`.
    fn expr_bp(&mut self, min: u8) -> R<Expr> {
        let mut lhs = self.prefix()?;
        while let Some((op, bp)) = binop(self.peek()) {
            if bp < min {
                break;
            }
            self.bump();
            let rhs = self.expr_bp(bp + 1)?; // + 1: the operators are left-associative
            let span = join(lhs.span, rhs.span);
            lhs = Expr { kind: ExprKind::Binary(op, Box::new(lhs), Box::new(rhs)), span };
        }
        Ok(lhs)
    }

    fn prefix(&mut self) -> R<Expr> {
        let op = match self.peek() {
            T::Minus => UnOp::Neg,
            T::Bang => UnOp::Not,
            _ => return self.primary(),
        };
        let start = self.bump();
        let e = self.prefix()?;
        Ok(Expr { span: join(start, e.span), kind: ExprKind::Unary(op, Box::new(e)) })
    }

    fn primary(&mut self) -> R<Expr> {
        let start = self.span();
        let kind = match self.peek().clone() {
            T::Number(v) => {
                self.bump();
                ExprKind::Int(v)
            }
            T::True | T::False => {
                let b = *self.peek() == T::True;
                self.bump();
                ExprKind::Bool(b)
            }
            T::Ident(x) => {
                self.bump();
                match self.peek() {
                    T::LParen => {
                        self.bump();
                        let mut args = Vec::new();
                        while *self.peek() != T::RParen {
                            args.push(self.expr()?);
                            if *self.peek() != T::Comma {
                                break;
                            }
                            self.bump();
                        }
                        self.expect(T::RParen, "')'")?;
                        ExprKind::Call(x, args)
                    }
                    T::LBracket => {
                        self.bump();
                        let i = self.expr()?;
                        self.expect(T::RBracket, "']'")?;
                        ExprKind::Index(x, Box::new(i))
                    }
                    _ => ExprKind::Var(x),
                }
            }
            T::LParen => {
                self.bump();
                let e = self.expr()?;
                self.expect(T::RParen, "')'")?;
                return Ok(Expr { kind: e.kind, span: join(start, self.prev()) });
            }
            k => return self.error(format!("expected an expression, found {}", spell(&k))),
        };
        Ok(Expr { kind, span: join(start, self.prev()) })
    }
}

/// Lex and parse a whole source file: the program, or every error shown
/// with its line and a caret.
pub fn parse_source(src: &str, file: &str) -> Result<Program, String> {
    let toks = crate::lexer::lex(src).map_err(|e| crate::lexer::show_error(src, file, &e))?;
    let mut p = Parser::new(&toks);
    let prog = p.program();
    if p.errors.is_empty() {
        return Ok(prog);
    }
    Err(p.errors.iter().map(|e| show(src, file, e)).collect())
}

/// Lex and parse one expression (the whole input).
pub fn parse_expr(src: &str) -> Result<Expr, String> {
    let toks = crate::lexer::lex(src).map_err(|e| e.msg)?;
    let mut p = Parser::new(&toks);
    match p.expr() {
        Ok(e) if *p.peek() == T::Eof => Ok(e),
        Ok(_) => Err(format!("unexpected {} after the expression", spell(p.peek()))),
        Err(()) => Err(p.errors[0].msg.clone()),
    }
}

pub fn show(src: &str, file: &str, e: &ParseError) -> String {
    crate::lexer::show_error(src, file, &crate::lexer::LexError { msg: e.msg.clone(), span: e.span })
}
