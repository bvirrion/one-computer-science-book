// derive_demo.rs -- the typing derivation of a small program, built by
// the checker, one judgement per line.
#![allow(dead_code)]
#[path = "../../05-lambda-calculus/listings/lam.rs"]
mod lam;
#[path = "check.rs"]
mod check;

fn main() {
    let src = r"(\f: int -> int. f (f 3)) (\x: int. x * 2)";
    let e = lam::parse(src).expect("a program");
    let d = check::derive(&vec![], &e).expect("a well-typed program");
    let mut lines = vec![];
    check::print(&d, 0, &mut lines);
    for l in &lines {
        println!("{l}");
    }
    println!("{} judgements", lines.len());
}
