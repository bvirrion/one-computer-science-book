// factor_aba.rs: a DFA for the words over {a, b} that contain the factor aba (exercise 7).
// State i: the longest suffix of what was read that is a prefix of aba has length i;
// state 3: aba has been seen.
pub const DELTA: [[usize; 2]; 4] = [
    [1, 0], // "":  a starts the pattern, b does not
    [1, 2], // "a": a again keeps "a", b makes "ab"
    [3, 0], // "ab": a completes aba, b leaves nothing
    [3, 3], // found: stay
];

pub fn contains_aba(word: &str) -> bool {
    let mut q = 0;
    for c in word.chars() {
        q = DELTA[q][if c == 'a' { 0 } else { 1 }];
    }
    q == 3
}
