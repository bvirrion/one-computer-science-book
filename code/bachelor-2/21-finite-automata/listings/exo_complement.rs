// exo_complement.rs: swapping the accepting states of an incomplete automaton (exercise 2).
#[allow(dead_code)]
mod automaton;
use automaton::Dfa;

fn main() {
    // a b*: from 0, a leads to 1; 1 loops on b; no other transition
    let ab = Dfa { alphabet: vec!['a', 'b'], start: 0, accept: vec![false, true],
                   delta: vec![vec![Some(1), None], vec![None, Some(1)]] };
    let swapped = Dfa { alphabet: ab.alphabet.clone(), delta: ab.delta.clone(),
                            start: 0, accept: vec![true, false] };
    let right = ab.complement();
    println!("word   a b*    swapped  complement");
    for w in ["", "a", "b", "ab", "ba", "abb", "aab"] {
        println!("{:6} {:7} {:8} {}", format!("{w:?}"), ab.accepts(w), swapped.accepts(w),
                 right.accepts(w));
    }
}
