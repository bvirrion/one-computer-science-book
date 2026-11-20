// longest.rs: a function returning one of two references must say how long the result lives.
pub fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    // the result lives as long as the shorter-lived of x and y
    if x.len() >= y.len() {
        x
    } else {
        y
    }
}

pub fn first_letter(s: &str) -> &str {
    // elided: one input reference, so the output borrows from it
    match s.char_indices().nth(1) {
        Some((i, _)) => &s[..i],
        None => s,
    }
}

#[allow(dead_code)]
fn main() {
    let a = String::from("Orchard Way");
    let result;
    {
        let b = String::from("Mill Row");
        println!("{}", longest(&a, &b)); // used while both live: fine
        result = first_letter(&a);
    }
    println!("{result}"); // borrows only from a, which still lives
}
