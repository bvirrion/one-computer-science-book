// count_trees.rs: parse trees of a+a+...+a in E -> E + E | a, and the Catalan numbers.
#[allow(dead_code)]
mod count;
#[allow(dead_code)]
mod grammar;

fn main() {
    let g = grammar::Grammar::parse("E -> E + E | a");
    let mut catalan: u128 = 1; // C_0
    println!("operands  trees          Catalan C(k - 1)");
    for k in 1..=20u128 {
        let word = vec!["a"; k as usize].join("+");
        let trees = count::trees(&g, &word);
        if k <= 8 || k % 4 == 0 {
            println!("{k:8}  {trees:<14} {catalan}");
        }
        assert_eq!(trees, catalan);
        catalan = catalan * 2 * (2 * k - 1) / (k + 1); // C_k from C_(k-1)
    }
}
