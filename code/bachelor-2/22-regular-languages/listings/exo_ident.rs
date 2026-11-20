// exo_ident.rs: an identifier pattern that lets a digit start the name (exercise 2).
#[allow(dead_code)]
mod regex;

fn main() {
    let compile = |p: &str| regex::Matcher::new(&regex::glushkov(&regex::parse(p).unwrap()));
    let (wrong, right) = (compile("[a-z0-9_]+"), compile("[a-z_][a-z0-9_]*"));
    for w in ["x", "x9", "9lives", "_tmp", "2", ""] {
        println!("{:9} [a-z0-9_]+ {:5}   [a-z_][a-z0-9_]* {}", format!("{w:?}"),
                 wrong.matches(w), right.matches(w));
    }
}
