// ex11_nested.rs -- skip a nested comment /* ... /* ... */ ... */ with a
// depth counter. Returns the length of the comment at the start of `s`.
#![allow(dead_code)]
pub fn nested_comment(s: &[u8]) -> Result<usize, String> {
    let (mut depth, mut i) = (0usize, 0);
    while i + 1 < s.len() {
        match (s[i], s[i + 1]) {
            (b'/', b'*') => {
                depth += 1;
                i += 2;
            }
            (b'*', b'/') if depth > 0 => {
                depth -= 1;
                i += 2;
                if depth == 0 {
                    return Ok(i);
                }
            }
            _ if depth == 0 => return Err("not a comment".into()),
            _ => i += 1,
        }
    }
    Err("unterminated comment".into())
}
