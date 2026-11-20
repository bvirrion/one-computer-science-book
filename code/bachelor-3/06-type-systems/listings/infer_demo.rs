// infer_demo.rs -- the principal type of each let-bound name of a .lam
// program, as inference generalises it, then the program's type.
// capture: args=poly.lam
#![allow(dead_code)]
#[path = "../../05-lambda-calculus/listings/lam.rs"]
mod lam;
#[path = "unify.rs"]
mod unify;
#[path = "infer.rs"]
mod infer;

fn main() {
    let file = std::env::args().nth(1).expect("usage: infer_demo FILE.lam");
    let e = lam::parse(&std::fs::read_to_string(&file).expect("a file")).expect("a program");
    let mut show = |name: &str, sc: &infer::Scheme| {
        let t = unify::normalise(&sc.ty);
        let mut vars = std::collections::BTreeSet::new();
        unify::type_vars(&t, &mut vars); // all quantified: the program has no free names
        let names: Vec<String> = vars.iter().map(|&v| lam::show_ty(&lam::Ty::Var(v))).collect();
        let forall = if sc.vars.is_empty() { String::new() } else {
            format!("forall {}. ", names.join(" "))
        };
        println!("{name:<8} : {forall}{}", lam::show_ty(&t));
    };
    let mut inf = infer::Infer::new(&mut show);
    let t = inf.infer(&vec![], &e).unwrap_or_else(|m| panic!("{m}"));
    println!("program  : {}", lam::show_ty(&unify::normalise(&t)));
}
