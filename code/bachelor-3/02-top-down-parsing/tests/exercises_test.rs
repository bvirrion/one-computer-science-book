// Tests of the programmed exercises.
#[path = "../exercises/ex12_userops.rs"]
mod ex12_userops;
#[path = "../exercises/ex5_minus_fixed.rs"]
mod ex5_minus_fixed;
use ex12_userops::{Assoc, Ops};

#[test]
fn ex5_minus_is_left_associative() {
    use ex5_minus_fixed::calc;
    assert_eq!(calc("8-4-2"), 2);
    assert_eq!(calc("8/4/2"), 1);
    assert_eq!(calc("9-2*3-1"), 2);
    assert_eq!(calc("1+2*3"), 7);
}

fn ops() -> Ops {
    let mut o = Ops::new();
    o.declare("or", 1, Assoc::Left);
    o.declare("==", 2, Assoc::Non);
    o.declare("+", 3, Assoc::Left);
    o.declare("-", 3, Assoc::Left);
    o.declare("*", 4, Assoc::Left);
    o.declare("^", 5, Assoc::Right);
    o.declare("::", 2, Assoc::Right);
    o
}

#[test]
fn ex12_user_declared_operators() {
    let o = ops();
    assert_eq!(o.parse("a - b - c").unwrap(), "(- (- a b) c)");
    assert_eq!(o.parse("a ^ b ^ c").unwrap(), "(^ a (^ b c))");
    assert_eq!(o.parse("x :: y :: z").unwrap(), "(:: x (:: y z))");
    assert_eq!(o.parse("a + b * c ^ d").unwrap(), "(+ a (* b (^ c d)))");
    assert_eq!(o.parse("( a + b ) * c").unwrap(), "(* (+ a b) c)");
    assert_eq!(o.parse("a == b or c").unwrap(), "(or (== a b) c)");
    assert!(o.parse("a == b == c").unwrap_err().contains("not associative"));
    assert!(o.parse("a + * b").is_err());
    assert!(o.parse("a b").is_err());
}
