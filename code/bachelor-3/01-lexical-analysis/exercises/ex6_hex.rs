// ex6_hex.rs -- Moor number literals with hexadecimal: 255, 0xff, 0XFF.
// Returns the value and the length of the literal at the start of `s`.
#![allow(dead_code)]
pub fn number(s: &[u8]) -> Result<(i64, usize), String> {
    let hex = s.len() >= 2 && s[0] == b'0' && (s[1] == b'x' || s[1] == b'X');
    let (radix, skip) = if hex { (16, 2) } else { (10, 0) };
    let digits = s[skip..].iter().take_while(|c| (**c as char).is_digit(radix)).count();
    if digits == 0 {
        return Err("a hexadecimal literal needs a digit after 0x".into());
    }
    let len = skip + digits;
    if s.get(len).is_some_and(|c| c.is_ascii_alphanumeric() || *c == b'_') {
        return Err(format!("bad digit '{}' in a number", s[len] as char));
    }
    let text = std::str::from_utf8(&s[skip..len]).unwrap();
    match i64::from_str_radix(text, radix) {
        Ok(v) if v <= u32::MAX as i64 && (hex || v <= i32::MAX as i64) => Ok((v, len)),
        _ => Err("number too large".into()),
    }
}
