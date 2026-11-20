// reverse_words.rs: reverse the order of the words of a String, in its own buffer (exercise 9).
pub fn reverse_words(s: String) -> String {
    let mut b = s.into_bytes(); // the same buffer, now seen as bytes: no copy
    b.reverse(); // the whole text backwards: words in the right order, each one backwards
    for word in b.split_mut(|&c| c == b' ') {
        word.reverse(); // each word forwards again, its multi-byte characters too
    }
    // every character's bytes were reversed exactly twice: the bytes are valid UTF-8 again
    String::from_utf8(b).expect("reversed twice, so valid")
}
