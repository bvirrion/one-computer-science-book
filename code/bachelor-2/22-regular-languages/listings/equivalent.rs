// equivalent.rs: do two expressions denote the same language? If not, a shortest witness.
#[allow(dead_code)]
mod dfa;
#[allow(dead_code)]
mod regex;

fn automaton(text: &str) -> dfa::Dfa {
    dfa::determinise(&regex::glushkov(&regex::parse(text).unwrap()), &['a', 'b'])
}

fn main() {
    for (x, y) in [("(a|b)*", "(a*b*)*"), ("(ab)*a", "a(ba)*"), ("a*b*", "(a|b)*"),
                   ("(a|b)*abb", "(a|b)*bb"), ("(aa|a)*", "a*")] {
        match dfa::difference(&automaton(x), &automaton(y)) {
            None => println!("{x:10} = {y}"),
            Some(w) => println!("{x:10} differs from {y}: on {w:?}"),
        }
    }
}
