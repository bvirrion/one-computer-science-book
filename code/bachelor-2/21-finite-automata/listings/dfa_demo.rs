// dfa_demo.rs: is the string a decimal number such as -12.5e3? One table and one loop.
const START: usize = 0;
const ACCEPT: [bool; 8] = [false, false, true, false, true, false, false, true];
// columns: digit, sign, point, e or E; rows: the 8 states; NO: no transition
const NO: usize = usize::MAX;
const TABLE: [[usize; 4]; 8] = [
    [2, 1, NO, NO],  // 0 start
    [2, NO, NO, NO], // 1 after the sign
    [2, NO, 3, 5],   // 2 in the integer part (accepting)
    [4, NO, NO, NO], // 3 after the point
    [4, NO, NO, 5],  // 4 in the fraction (accepting)
    [7, 6, NO, NO],  // 5 after the e
    [7, NO, NO, NO], // 6 after the exponent's sign
    [7, NO, NO, NO], // 7 in the exponent (accepting)
];

pub fn class(c: char) -> Option<usize> {
    match c {
        '0'..='9' => Some(0),
        '+' | '-' => Some(1),
        '.' => Some(2),
        'e' | 'E' => Some(3),
        _ => None,
    }
}

pub fn is_number(s: &str) -> (bool, Vec<usize>) {
    let (mut q, mut path) = (START, vec![START]);
    for c in s.chars() {
        match class(c).map(|k| TABLE[q][k]) {
            Some(next) if next != NO => q = next,
            _ => return (false, path), // no transition: rejected at once
        }
        path.push(q);
    }
    (ACCEPT[q], path)
}

fn main() {
    for s in ["-12.5e3", "+0.25E-7", "42", "3.", ".5", "1e", "12a", "--1", ""] {
        let (ok, path) = is_number(s);
        let path: Vec<String> = path.iter().map(|q| q.to_string()).collect();
        let verdict = if ok { "number" } else { "no" };
        println!("{:10} {verdict:8} states {}", format!("{s:?}"), path.join(" "));
    }
}
