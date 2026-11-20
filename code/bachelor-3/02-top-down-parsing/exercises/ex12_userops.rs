// ex12_userops.rs -- precedence climbing over operators declared at run
// time, each with a binding power and an associativity. Operands are names
// or numbers, tokens are separated by spaces; the result is an S-expression.
#![allow(dead_code)]
use std::collections::HashMap;

#[derive(Clone, Copy, PartialEq)]
pub enum Assoc { Left, Right, Non }

pub struct Ops {
    table: HashMap<String, (u8, Assoc)>,
}

impl Ops {
    pub fn new() -> Self {
        Ops { table: HashMap::new() }
    }
    pub fn declare(&mut self, op: &str, bp: u8, assoc: Assoc) {
        assert!(bp >= 1);
        self.table.insert(op.to_string(), (bp, assoc));
    }

    pub fn parse(&self, src: &str) -> Result<String, String> {
        let toks: Vec<&str> = src.split_whitespace().collect();
        let mut pos = 0;
        let e = self.expr(&toks, &mut pos, 1)?;
        match toks.get(pos) {
            None => Ok(e),
            Some(t) => Err(format!("unexpected '{t}'")),
        }
    }

    fn expr(&self, toks: &[&str], pos: &mut usize, min: u8) -> Result<String, String> {
        let mut lhs = self.primary(toks, pos)?;
        let mut last_non: Option<u8> = None; // a non-associative level already used here
        while let Some(&(bp, assoc)) = toks.get(*pos).and_then(|t| self.table.get(*t)) {
            if bp < min {
                break;
            }
            if last_non == Some(bp) {
                return Err(format!("operator '{}' is not associative", toks[*pos]));
            }
            let op = toks[*pos];
            *pos += 1;
            let next = if assoc == Assoc::Right { bp } else { bp + 1 };
            let rhs = self.expr(toks, pos, next)?;
            lhs = format!("({op} {lhs} {rhs})");
            last_non = if assoc == Assoc::Non { Some(bp) } else { None };
        }
        Ok(lhs)
    }

    fn primary(&self, toks: &[&str], pos: &mut usize) -> Result<String, String> {
        match toks.get(*pos) {
            Some(&"(") => {
                *pos += 1;
                let e = self.expr(toks, pos, 1)?;
                if toks.get(*pos) != Some(&")") {
                    return Err("expected ')'".into());
                }
                *pos += 1;
                Ok(e)
            }
            Some(t) if !self.table.contains_key(*t) && *t != ")" => {
                *pos += 1;
                Ok(t.to_string())
            }
            Some(t) => Err(format!("expected an operand, found '{t}'")),
            None => Err("expected an operand, found the end".into()),
        }
    }
}

impl Default for Ops {
    fn default() -> Self {
        Self::new()
    }
}
