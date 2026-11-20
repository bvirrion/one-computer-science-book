// multiples.rs: the multiples of n written in base b, as a DFA on the digits (exercise 9).
// The state is the value read so far, modulo n: reading digit d sends r to (b r + d) mod n.

pub fn delta(n: u32, b: u32) -> Vec<Vec<u32>> {
    (0..n).map(|r| (0..b).map(|d| (b * r + d) % n).collect()).collect()
}

/// digits: most significant first; the empty word stands for 0.
pub fn is_multiple(n: u32, b: u32, digits: &[u32]) -> bool {
    let table = delta(n, b);
    digits.iter().fold(0, |r, &d| table[r as usize][d as usize]) == 0
}
