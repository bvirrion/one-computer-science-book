// simulate_vs_determinise.rs: simulate the NFA letter by letter, or build the DFA first?
#[allow(dead_code)]
mod automaton;
use automaton::{kth_from_end, Nfa};
use std::time::Instant;

/// Simulation with the set of states as the bits of one machine word.
fn simulate_bits(n: &Nfa, word: &[usize]) -> bool {
    let mut masks = vec![[0u64; 2]; n.delta.len()]; // successors of q on a and on b
    for (q, row) in n.delta.iter().enumerate() {
        for a in 0..2 {
            masks[q][a] = row[a].iter().fold(0, |m, &r| m | 1 << r);
        }
    }
    let mut set = 1u64 << n.start[0];
    for &a in word {
        let mut next = 0;
        let mut rest = set;
        while rest != 0 {
            let q = rest.trailing_zeros() as usize; // one state of the set
            next |= masks[q][a];
            rest &= rest - 1;
        }
        set = next;
    }
    (0..n.delta.len()).any(|q| set >> q & 1 == 1 && n.accept[q])
}

fn main() {
    let mut x: u64 = 12345; // a fixed pseudo-random word of 2 million letters
    let word: Vec<usize> = (0..2_000_000).map(|_| {
        x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (x >> 63) as usize
    }).collect();
    let text: String = word.iter().map(|&a| if a == 0 { 'a' } else { 'b' }).collect();
    println!("  k   NFA, sets    NFA, bits   DFA states   build (ms)          DFA");
    println!("     ns/letter    ns/letter                             ns/letter");
    for k in [4, 10, 16] {
        let n = kth_from_end(k);
        let t = Instant::now();
        let r1 = n.accepts(&text[..200_000]); // sets of states as BTreeSets
        let sets_ns = t.elapsed().as_nanos() as f64 / 200_000.0;
        let t = Instant::now();
        let r2 = simulate_bits(&n, &word);
        let bits_ns = t.elapsed().as_nanos() as f64 / 2e6;
        let t = Instant::now();
        let (dfa, _) = n.determinise();
        let build_ms = t.elapsed().as_secs_f64() * 1e3;
        let t = Instant::now();
        let mut q = dfa.start;
        for &a in &word {
            q = dfa.delta[q][a].unwrap();
        }
        let dfa_ns = t.elapsed().as_nanos() as f64 / 2e6;
        assert!(r1 == n.accepts(&text[..200_000]) && r2 == dfa.accept[q]);
        println!("{k:3} {sets_ns:12.0} {bits_ns:12.1} {:12} {build_ms:12.1} {dfa_ns:12.1}",
                 dfa.delta.len());
    }
}
