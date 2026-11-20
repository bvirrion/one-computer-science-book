// Tests of the programmed exercises.
#[path = "../exercises/ex11_nested.rs"]
mod ex11_nested;
#[path = "../exercises/ex5_words_fixed.rs"]
mod ex5_words_fixed;
#[path = "../exercises/ex6_hex.rs"]
mod ex6_hex;

#[test]
fn ex5_keeps_the_last_word() {
    assert_eq!(ex5_words_fixed::words("var n = 7"), vec!["var", "n", "7"]);
    assert_eq!(ex5_words_fixed::words("var n = 7;\n"), vec!["var", "n", "7"]);
    assert!(ex5_words_fixed::words("").is_empty());
}

#[test]
fn ex6_hexadecimal_literals() {
    use ex6_hex::number;
    assert_eq!(number(b"255;"), Ok((255, 3)));
    assert_eq!(number(b"0xff)"), Ok((255, 4)));
    assert_eq!(number(b"0XFFFFFFFF"), Ok((4294967295, 10)));
    assert_eq!(number(b"0"), Ok((0, 1)));
    assert!(number(b"0x").is_err());
    assert!(number(b"0x1g").is_err());
    assert!(number(b"0x100000000").is_err());
    assert!(number(b"2147483648").is_err());
}

#[test]
fn ex11_nested_comments() {
    use ex11_nested::nested_comment;
    assert_eq!(nested_comment(b"/* a */ x"), Ok(7));
    assert_eq!(nested_comment(b"/* a /* b */ c */ x"), Ok(17));
    assert!(nested_comment(b"/* /* */").is_err());
    assert!(nested_comment(b"x /* */").is_err());
}
