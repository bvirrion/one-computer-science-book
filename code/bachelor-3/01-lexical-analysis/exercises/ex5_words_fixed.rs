// ex5_words_fixed.rs -- the scanner of words_bug.rs, fixed: the word under
// construction when the input ends is a token too.
#![allow(dead_code)]
pub fn words(src: &str) -> Vec<String> {
    let mut out = Vec::new();
    let mut current = String::new();
    for c in src.chars() {
        if c.is_ascii_alphanumeric() {
            current.push(c);
        } else if !current.is_empty() {
            out.push(std::mem::take(&mut current));
        }
    }
    if !current.is_empty() {
        out.push(current);
    }
    out
}
