// exo_pda_equal.rs: a pushdown automaton for the words with as many a as b (exercise 9).
#[allow(dead_code)]
mod grammar;
#[allow(dead_code)]
mod pda;
use pda::{Move, Pda};

fn main() {
    let mv = |read, pop, push: &str| Move { from: 0, read: Some(read), pop, to: 0,
                                           push: push.chars().collect() };
    let mut moves = vec![
        mv('a', 'Z', "AZ"), mv('a', 'A', "AA"), mv('a', 'B', ""), // the stack holds the
        mv('b', 'Z', "BZ"), mv('b', 'B', "BB"), mv('b', 'A', ""), // surplus: A's or B's
    ];
    moves.push(Move { from: 0, read: None, pop: 'Z', to: 1, push: vec!['Z'] });
    let equal = Pda { start: 0, bottom: 'Z', accept: vec![1], moves };
    let mut checked = 0;
    for n in 0..=10 {
        for m in 0..1u32 << n {
            let w: String = (0..n).map(|i| if m >> i & 1 == 0 { 'a' } else { 'b' }).collect();
            let want = w.matches('a').count() == w.matches('b').count();
            assert_eq!(equal.accepts(&w, n + 1).0, want, "{w}");
            checked += 1;
        }
    }
    println!("{checked} words up to length 10: accepted exactly when as many a as b");
    for w in ["abba", "aabbb", "babaab"] {
        println!("{w:7} {}", equal.accepts(w, 10).0);
    }
}
