// words_bug.rs -- a first scanner for words and numbers. It has a bug.
fn words(src: &str) -> Vec<String> {
    let mut out = Vec::new();
    let mut current = String::new();
    for c in src.chars() {
        if c.is_ascii_alphanumeric() {
            current.push(c);
        } else if !current.is_empty() {
            out.push(current.clone());
            current.clear();
        }
    }
    out
}

fn main() {
    println!("{:?}", words("var n = 7;\n"));
    println!("{:?}", words("var n = 7"));
}
