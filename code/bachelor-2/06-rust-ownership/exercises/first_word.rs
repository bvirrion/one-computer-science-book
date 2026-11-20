// first_word.rs: the first word of a string, borrowed from it (exercise 3).
pub fn first_word(s: &str) -> &str {
    // up to the first whitespace character, or the whole string
    match s.find(char::is_whitespace) {
        Some(i) => &s[..i], // i is the byte index of a character: always a boundary
        None => s,
    }
}
