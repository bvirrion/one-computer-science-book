// exo_eliminate.rs: state elimination on "an even number of a" (exercise 7).
#[allow(dead_code)]
mod dfa;
#[allow(dead_code)]
mod regex;

fn main() {
    let even = dfa::Dfa { alphabet: vec!['a', 'b'], accept: vec![true, false],
                          delta: vec![vec![1, 0], vec![0, 1]] };
    let re = dfa::eliminate(&even);
    println!("{}", re.show());
    let m = regex::Matcher::new(&regex::glushkov(&re));
    let all = regex::lang(&regex::parse("(a|b)*").unwrap(), 10);
    let ok = all.iter().all(|w| m.matches(w) == (w.matches('a').count() % 2 == 0));
    println!("right on all {} words up to length 10: {ok}", all.len());
}
