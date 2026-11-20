// The weekend problem's numbers (solutions/02-top-down-parsing.tex).
#[path = "../exercises/pb_fines.rs"]
mod pb_fines;
use pb_fines::{both, eval, Tree};

pub const FINE: &str =
    "max(0, days - 14) * rate + 2 ^ late ^ 2 * (items > 3) + 10 * (lost or damaged and items >= 1)";

#[test]
fn the_fines_formula() {
    let (a, rd, b, pc) = both(FINE);
    assert_eq!(a, b);
    assert_eq!((rd, pc), (80, 34));
    let env = |x: &str| match x {
        "days" => 20, "rate" => 3, "late" => 1, "items" => 4, "lost" => 0, "damaged" => 1, _ => 0,
    };
    assert_eq!(eval(&a, &env), 30);
}

#[test]
fn power_is_right_associative() {
    let (a, _, _, _) = both("2 ^ 3 ^ 2");
    assert_eq!(eval(&a, &|_| 0), 512);
    let (b, _, _, _) = both("10 - 4 - 3");
    assert_eq!(eval(&b, &|_| 0), 3);
    assert!(matches!(a, Tree::Op(_, _, _)));
}

#[test]
fn calls_on_chains() {
    for n in 1..=100usize {
        let or_chain = vec!["x"; n].join(" or ");
        let (_, rd, _, pc) = both(&or_chain);
        assert_eq!((rd, pc), (7 * n + 1, 2 * n));
        let plus_chain = vec!["x"; n].join(" + ");
        let (_, rd, _, pc) = both(&plus_chain);
        assert_eq!((rd, pc), (3 * n + 5, 2 * n));
        let pow_chain = vec!["x"; n].join(" ^ ");
        let (_, rd, _, pc) = both(&pow_chain);
        assert_eq!((rd, pc), (2 * n + 6, 2 * n));
    }
}

#[test]
fn both_parsers_agree_on_random_formulas() {
    let ops = ["or", "and", "==", "<", ">=", "+", "-", "*", "/", "^"];
    let mut seed: u64 = 11;
    for _ in 0..2000 {
        let mut s = String::from("a");
        for _ in 0..7 {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            s += &format!(" {} b", ops[(seed >> 33) as usize % ops.len()]);
        }
        let (a, _, b, _) = both(&s);
        assert_eq!(a, b, "{s}");
    }
}
