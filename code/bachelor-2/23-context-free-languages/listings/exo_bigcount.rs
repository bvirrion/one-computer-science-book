// exo_bigcount.rs: parse trees of a+a+...+a with up to 100 operands, against Catalan.
#[allow(dead_code)]
mod grammar;
#[path = "../exercises/bigcount.rs"]
mod bigcount;
use bigcount::Big;

fn main() {
    let g = grammar::Grammar::parse("E -> E + E | a").cnf();
    let mut catalan = Big::small(1); // C_0
    for k in 1..=100u32 {
        if [10, 25, 50, 100].contains(&k) {
            let trees = bigcount::trees(&g, &vec!["a"; k as usize].join("+"));
            let digits = trees.decimal();
            println!("{k:3} operands: {} digits, {}..., equal to C({}): {}", digits.len(),
                     &digits[..digits.len().min(12)], k - 1, trees == catalan);
        }
        let (c, rest) = catalan.mul(&Big::small(2 * (2 * k - 1))).div_small(k + 1);
        assert_eq!(rest, 0); // C_k = C_(k-1) 2(2k - 1) / (k + 1), exactly
        catalan = c;
    }
}
