// semantics_demo.rs -- run a .lam program by the small-step rules (every
// step printed) and by the big-step rules (the derivation's size).
// capture: args=sum.lam
#![allow(dead_code)]
#[path = "lam.rs"]
mod lam;
#[path = "smallstep.rs"]
mod smallstep;
#[path = "bigstep.rs"]
mod bigstep;

fn main() {
    let file = std::env::args().nth(1).expect("usage: semantics_demo FILE.lam");
    let src = std::fs::read_to_string(&file).expect("a readable file");
    let e = lam::parse(&src).unwrap_or_else(|m| panic!("{file}: {m}"));
    // Print the unfolded recursive function as <f>, and its letrec as "...".
    let mut short: Vec<(String, String)> = vec![];
    if let lam::E::LetRec(f, l, _) = &e {
        let unf = lam::show(&smallstep::unfold(f, l));
        short.push((format!("({unf})"), format!("<{f}>")));
        short.push((unf, format!("<{f}>")));
        short.push((format!("letrec {f} = {} in ", lam::show(l)), format!("letrec {f} = ... in ")));
    }
    let (small, steps) = smallstep::run(&e, 100_000, &mut |n, t| {
        let mut s = lam::show(t);
        if n > 0 {
            for (long, abbrev) in &short {
                s = s.replace(long.as_str(), abbrev);
            }
        }
        let s = if s.chars().count() > 86 { s.chars().take(83).collect::<String>() + "..." } else { s };
        println!("{n:>3}  {s}");
    });
    println!("small-step: {} after {steps} steps", lam::show(&small.clone().unwrap()));
    let mut z = bigstep::Size::default();
    let big = bigstep::eval(&e, &mut z, 0).unwrap();
    println!("big-step:   {} by a derivation of {} nodes, {} of them contractions, depth {}",
             lam::show(&big), z.nodes, z.contractions, z.depth);
}
