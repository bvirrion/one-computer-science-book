// ex5_minus_fixed.rs -- minus_bug.rs fixed: the right operand of a
// left-associative operator may only contain tighter operators (p + 1).
#![allow(dead_code)]
fn bp(op: char) -> Option<u8> {
    match op {
        '+' | '-' => Some(1),
        '*' | '/' => Some(2),
        _ => None,
    }
}

pub fn expr(toks: &[char], pos: &mut usize, min: u8) -> i64 {
    let mut lhs = toks[*pos].to_digit(10).unwrap() as i64;
    *pos += 1;
    while let Some(&op) = toks.get(*pos) {
        let Some(p) = bp(op) else { break };
        if p < min {
            break;
        }
        *pos += 1;
        let rhs = expr(toks, pos, p + 1);
        lhs = match op { '+' => lhs + rhs, '-' => lhs - rhs, '*' => lhs * rhs, _ => lhs / rhs };
    }
    lhs
}

pub fn calc(s: &str) -> i64 {
    let toks: Vec<char> = s.chars().collect();
    expr(&toks, &mut 0, 1)
}
