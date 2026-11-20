// product.rs: "even length" and "starts with a", run together; then the useless pairs.
#[allow(dead_code)]
mod automaton;
use automaton::{product, Dfa};

fn main() {
    let even = Dfa { alphabet: vec!['a', 'b'], start: 0, accept: vec![true, false],
                     delta: vec![vec![Some(1), Some(1)], vec![Some(0), Some(0)]] };
    let starts_a = Dfa { alphabet: vec!['a', 'b'], start: 0, accept: vec![false, true, false],
                         // 0 start, 1 began with a, 2 began with b (a sink)
                         delta: vec![vec![Some(1), Some(2)], vec![Some(1), Some(1)],
                                     vec![Some(2), Some(2)]] };
    let both = product(&even, &starts_a, true);
    let (acc, co) = (both.accessible(), both.co_accessible());
    println!("pair    on a    on b    accepting  accessible  co-accessible");
    for (i, row) in both.delta.iter().enumerate() {
        let name = |s: usize| format!("({},{})", s / 3, s % 3);
        println!("{:7} {:7} {:7} {:10} {:11} {}", name(i), name(row[0].unwrap()),
                 name(row[1].unwrap()), both.accept[i], acc[i], co[i]);
    }
    let useful = (0..6).filter(|&i| acc[i] && co[i]).count();
    println!("trim automaton: {useful} of 6 states");
    let counts = both.count_accepted(8);
    println!("accepted words of length 0..8: {counts:?}");
}
