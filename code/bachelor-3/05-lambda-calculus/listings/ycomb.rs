// ycomb.rs -- recursion without names: factorial through Y and through Z
// under call by value, and through letrec for comparison.
#![allow(dead_code)]
#[path = "lam.rs"]
mod lam;
#[path = "smallstep.rs"]
mod smallstep;

const Y: &str = r"\f. (\x. f (x x)) (\x. f (x x))";
const Z: &str = r"\f. (\x. f (\v. x x v)) (\x. f (\v. x x v))";
const F: &str = r"\fact. \n. if n == 0 then 1 else n * fact (n - 1)";

fn size(e: &lam::E) -> usize {
    lam::show(e).len() // a crude but monotone measure: printed length
}

fn main() {
    let programs = [
        ("Z F 5", format!("({Z}) ({F}) 5")),
        ("letrec", format!("letrec fact = {} in fact 5", &F[7..])),
        ("Y F 5", format!("({Y}) ({F}) 5")),
    ];
    for (name, src) in programs {
        let e = lam::parse(&src).expect("a program");
        let mut last = 0;
        let (r, steps) = smallstep::run(&e, 2_000, &mut |_, t| last = size(t));
        match r {
            Ok(v) => println!("{name:<7} value {} after {steps} steps", lam::show(&v)),
            Err(m) => println!("{name:<7} {m}; the term is now {last} characters long"),
        }
    }
}
