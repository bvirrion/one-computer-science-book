// occurs.rs -- terms whose inference fails, and why.
#![allow(dead_code)]
#[path = "../../05-lambda-calculus/listings/lam.rs"]
mod lam;
#[path = "unify.rs"]
mod unify;
#[path = "infer.rs"]
mod infer;

fn main() {
    for src in [r"\x. x x", r"\f. (\x. f (x x)) (\x. f (x x))",
                r"(\id. (id 1, id true)) (\x. x)", r"let id = \x. x in (id 1, id true)"] {
        match infer::principal(&lam::parse(src).unwrap()) {
            Ok(t) => println!("{src}\n    : {}", lam::show_ty(&t)),
            Err(m) => println!("{src}\n    {m}"),
        }
    }
}
