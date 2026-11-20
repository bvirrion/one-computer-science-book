// ex12_oracle.rs -- exercise 12: random Moor programs, to compare the
// compiled code with the interpreter.
#![allow(dead_code)]

pub struct Rng(pub u64);
impl Rng {
    pub fn below(&mut self, n: u64) -> u64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (self.0 >> 33) % n
    }
}

const VARS: [&str; 3] = ["a", "b", "c"];

fn expr(r: &mut Rng, depth: u32) -> String {
    if depth == 0 || r.below(3) == 0 {
        return if r.below(2) == 0 {
            VARS[r.below(3) as usize].to_string()
        } else {
            (r.below(41) as i64 - 20).to_string()
        };
    }
    let op = ["+", "-", "*", "/", "+", "*"][r.below(6) as usize];
    format!("({} {op} {})", expr(r, depth - 1), expr(r, depth - 1))
}

fn cond(r: &mut Rng) -> String {
    let rel = ["<", "<=", ">", ">=", "==", "!="][r.below(6) as usize];
    let c = format!("{} {rel} {}", expr(r, 2), expr(r, 2));
    match r.below(4) {
        0 => format!("{c} && {} < {}", expr(r, 1), expr(r, 1)),
        1 => format!("!({c}) || {} == {}", expr(r, 1), expr(r, 1)),
        _ => c,
    }
}

fn stmts(r: &mut Rng, depth: u32, out: &mut Vec<String>, loops: &mut u32) {
    for _ in 0..1 + r.below(4) {
        let v = VARS[r.below(3) as usize];
        match r.below(6) {
            0 if depth > 0 => {
                out.push(format!("if {} {{", cond(r)));
                stmts(r, depth - 1, out, loops);
                out.push("} else {".into());
                stmts(r, depth - 1, out, loops);
                out.push("}".into());
            }
            1 if depth > 0 => {
                *loops += 1;
                let k = format!("k{loops}");
                out.push(format!("var {k} = 0;"));
                out.push(format!("while {k} < {} && {} {{", 1 + r.below(5), cond(r)));
                stmts(r, depth - 1, out, loops);
                out.push(format!("{k} = {k} + 1;"));
                out.push("}".into());
            }
            2 => out.push(format!("print({v});")),
            _ => out.push(format!("{v} = {};", expr(r, 3))),
        }
    }
}

/// A program of three variables, a few statements, and a printed result.
pub fn program(seed: u64) -> String {
    let mut r = Rng(seed);
    let mut body = vec![];
    for v in VARS {
        body.push(format!("var {v} = {};", r.below(21) as i64 - 10));
    }
    let mut loops = 0;
    stmts(&mut r, 2, &mut body, &mut loops);
    body.push("print(a); print(b); print(c);".into());
    body.push("return a + b * c;".into());
    format!("fn main() -> int {{\n    {}\n}}\n", body.join("\n    "))
}
