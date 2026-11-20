// ex6_church.rs -- exercise 6: a test for zero and equality of numerals,
// written with the definitions of encode.rs.
#![allow(dead_code)]

pub const SUB: &str = r"\m n. n pred m";
pub const IS_ZERO: &str = r"\n. n (\x. false) true";
/// m = n when both m - n and n - m are zero (subtraction stops at zero).
pub const AND: &str = r"\p q. p q false";

pub fn eq_src() -> String {
    format!(r"\m n. ({AND}) (({IS_ZERO}) (({SUB}) m n)) (({IS_ZERO}) (({SUB}) n m))")
}
