// minus_bug.rs -- a calculator by precedence climbing. It has a bug.
fn bp(op: char) -> Option<u8> {
    match op {
        '+' | '-' => Some(1),
        '*' | '/' => Some(2),
        _ => None,
    }
}

fn expr(toks: &[char], pos: &mut usize, min: u8) -> i64 {
    let mut lhs = toks[*pos].to_digit(10).unwrap() as i64;
    *pos += 1;
    while let Some(&op) = toks.get(*pos) {
        let Some(p) = bp(op) else { break };
        if p < min {
            break;
        }
        *pos += 1;
        let rhs = expr(toks, pos, p);
        lhs = match op { '+' => lhs + rhs, '-' => lhs - rhs, '*' => lhs * rhs, _ => lhs / rhs };
    }
    lhs
}

fn main() {
    for s in ["1+2*3", "2*3+1", "8-4-2", "8/4/2", "9-2*3-1"] {
        let toks: Vec<char> = s.chars().collect();
        println!("{s} = {}", expr(&toks, &mut 0, 1));
    }
}
