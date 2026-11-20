// exo_count.rs: how many words of each length avoid the factor bb (exercise 4)?
#[allow(dead_code)]
mod automaton;
use automaton::Dfa;

fn main() {
    // state 0: last letter not b (or no letter); 1: last letter b; 2: bb seen (a sink)
    let no_bb = Dfa { alphabet: vec!['a', 'b'], start: 0, accept: vec![true, true, false],
                      delta: vec![vec![Some(0), Some(1)], vec![Some(0), Some(2)],
                                  vec![Some(2), Some(2)]] };
    println!("{:?}", no_bb.count_accepted(15));
}
