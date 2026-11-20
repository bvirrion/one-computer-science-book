// ambiguity.rs: parse trees counted in two expression grammars and two if-else grammars.
#[allow(dead_code)]
mod grammar;
#[allow(dead_code)]
mod count;
use grammar::Grammar;

fn main() {
    let flat = Grammar::parse("E -> E + E | E * E | ( E ) | a");
    let levels = Grammar::parse("E -> E + T | T\nT -> T * F | F\nF -> ( E ) | a");
    println!("word        trees: flat  levels");
    for w in ["a+a*a", "a*a+a", "a+a+a", "a+a+a+a", "(a+a)*a"] {
        println!("{w:12} {:11} {:7}", count::trees(&flat, w), count::trees(&levels, w));
    }
    let same = flat.generated(7) == levels.generated(7);
    println!("same words up to length 7: {same}");
    let dangling = Grammar::parse("S -> i S | i S e S | x");
    let matched = Grammar::parse("S -> M | U\nM -> i M e M | x\nU -> i S | i M e U");
    println!("word        trees: dangling  matched");
    for w in ["ix", "ixex", "iixex", "iixexex", "iiixex"] {
        println!("{w:12} {:15} {:8}", count::trees(&dangling, w), count::trees(&matched, w));
    }
    println!("same words up to length 9: {}", dangling.generated(9) == matched.generated(9));
}
