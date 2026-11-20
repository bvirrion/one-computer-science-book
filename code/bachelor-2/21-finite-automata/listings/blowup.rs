// blowup.rs: k + 1 NFA states, 2^k DFA states; every pair of them is distinguishable.
#[allow(dead_code)]
mod automaton;
use automaton::kth_from_end;

fn main() {
    println!(" k  NFA states  DFA states   2^k  reached by the 2^k words  pairs told apart");
    for k in 1..=12 {
        let (dfa, _) = kth_from_end(k).determinise();
        // the 2^k words of length k, read as k bits (1 for a), first letter highest
        let state = |bits: usize| {
            dfa.run_from(dfa.start, &word(k, bits)).unwrap()
        };
        let reached: std::collections::HashSet<usize> = (0..1 << k).map(state).collect();
        println!("{k:2} {:11} {:11} {:5} {:25} {:17}", k + 1, dfa.delta.len(), 1 << k,
                 reached.len(), told_apart(k, &dfa));
    }
}

/// For two words u != v of length k, differing first at position i, the suffix b^i
/// puts u's letter at position i k-th from the end: one word is accepted, not the other.
fn told_apart(k: usize, dfa: &automaton::Dfa) -> usize {
    let mut pairs = 0;
    for u in 0..1usize << k {
        for v in u + 1..1 << k {
            let i = (u ^ v).leading_zeros() as usize - (usize::BITS as usize - k);
            let suffix = "b".repeat(i);
            let (wu, wv) = (word(k, u) + &suffix, word(k, v) + &suffix);
            assert_ne!(dfa.accepts(&wu), dfa.accepts(&wv));
            pairs += 1;
        }
    }
    pairs
}

/// The word of length k whose letters are the bits of `bits` (1 for a), highest first.
fn word(k: usize, bits: usize) -> String {
    (0..k).map(|i| if bits >> (k - 1 - i) & 1 == 1 { 'a' } else { 'b' }).collect()
}
