// exo_match.rs: which words does (ab|b)*a? match (exercise 1)?
#[allow(dead_code)]
mod regex;

fn main() {
    let m = regex::Matcher::new(&regex::glushkov(&regex::parse("(ab|b)*a?").unwrap()));
    for w in ["", "a", "aa", "bab", "abba", "babab", "aab"] {
        println!("{:8} {}", format!("{w:?}"), m.matches(w));
    }
}
