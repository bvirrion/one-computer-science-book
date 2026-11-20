//! Tests of chapter 21: the subset construction against simulation, the blow-up,
//! the closure constructions by brute force, and the exercises' automata.
#[allow(dead_code)]
#[path = "../../../listings/automaton.rs"]
pub mod automaton;
#[path = "../../../exercises/factor_aba.rs"]
pub mod factor_aba;
#[path = "../../../exercises/multiples.rs"]
pub mod multiples;

#[cfg(test)]
mod tests {
    use super::automaton::*;

    /// Every word over the alphabet up to length n.
    fn words(alphabet: &[char], n: usize) -> Vec<String> {
        let mut all = vec![String::new()];
        let mut layer = vec![String::new()];
        for _ in 0..n {
            layer = layer
                .iter()
                .flat_map(|w| alphabet.iter().map(move |c| format!("{w}{c}")))
                .collect();
            all.extend(layer.iter().cloned());
        }
        all
    }

    /// A small pseudo-random NFA with spontaneous transitions.
    fn random_nfa(seed: u64, states: usize, letters: usize) -> Nfa {
        let mut x = seed;
        let mut next = move || {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (x >> 33) as usize
        };
        let alphabet: Vec<char> = "abc".chars().take(letters).collect();
        let mut delta = vec![vec![vec![]; letters]; states];
        let mut eps = vec![vec![]; states];
        for q in 0..states {
            for row in delta[q].iter_mut() {
                for r in 0..states {
                    if next() % 4 == 0 {
                        row.push(r);
                    }
                }
            }
            for r in 0..states {
                if r != q && next() % 6 == 0 {
                    eps[q].push(r);
                }
            }
        }
        let accept = (0..states).map(|_| next() % 3 == 0).collect();
        Nfa { alphabet, delta, eps, start: vec![0], accept }
    }

    #[test]
    fn subset_construction_agrees_with_simulation() {
        for seed in 0..60 {
            let letters = 2 + (seed as usize % 2);
            let nfa = random_nfa(seed, 3 + seed as usize % 4, letters);
            let (dfa, subsets) = nfa.determinise();
            assert!(dfa.delta.len() <= 1 << nfa.delta.len());
            assert_eq!(subsets.len(), dfa.delta.len());
            let n = if letters == 2 { 10 } else { 7 };
            for w in words(&nfa.alphabet, n) {
                assert_eq!(nfa.accepts(&w), dfa.accepts(&w), "seed {seed}, word {w}");
            }
        }
    }

    #[test]
    fn blowup_exactly_two_to_the_k() {
        for k in 1..=10 {
            let (dfa, _) = kth_from_end(k).determinise();
            assert_eq!(dfa.delta.len(), 1 << k);
            for w in words(&['a', 'b'], k + 3) {
                let chars: Vec<char> = w.chars().collect();
                let truth = chars.len() >= k && chars[chars.len() - k] == 'a';
                assert_eq!(dfa.accepts(&w), truth);
            }
        }
    }

    fn even() -> Dfa {
        Dfa { alphabet: vec!['a', 'b'], start: 0, accept: vec![true, false],
              delta: vec![vec![Some(1), Some(1)], vec![Some(0), Some(0)]] }
    }

    fn ends_b() -> Dfa {
        Dfa { alphabet: vec!['a', 'b'], start: 0, accept: vec![false, true],
              delta: vec![vec![Some(0), Some(1)], vec![Some(0), Some(1)]] }
    }

    #[test]
    fn closure_constructions() {
        let (x, y) = (even(), ends_b());
        let (both, either, not_x) = (product(&x, &y, true), product(&x, &y, false), x.complement());
        for w in words(&['a', 'b'], 9) {
            assert_eq!(both.accepts(&w), x.accepts(&w) && y.accepts(&w));
            assert_eq!(either.accepts(&w), x.accepts(&w) || y.accepts(&w));
            assert_eq!(not_x.accepts(&w), !x.accepts(&w));
        }
    }

    #[test]
    fn trim_keeps_language_and_counts() {
        let x = even();
        let (acc, co) = (x.accessible(), x.co_accessible());
        assert!(acc.iter().all(|&a| a) && co.iter().all(|&c| c));
        let no_a = Dfa { alphabet: vec!['a', 'b'], start: 0, accept: vec![true, false],
                         delta: vec![vec![Some(1), Some(0)], vec![Some(1), Some(1)]] };
        assert_eq!(no_a.co_accessible(), vec![true, false]);
        assert_eq!(no_a.count_accepted(5), vec![1; 6]); // only b^n
    }

    #[test]
    fn exercises() {
        for w in words(&['a', 'b'], 10) {
            assert_eq!(super::factor_aba::contains_aba(&w), w.contains("aba"), "{w}");
        }
        for (n, b) in [(3, 2), (7, 10), (5, 3), (6, 4), (1, 2)] {
            for x in 0..2000u32 {
                let mut digits = vec![];
                let mut y = x;
                while y > 0 {
                    digits.insert(0, y % b);
                    y /= b;
                }
                assert_eq!(super::multiples::is_multiple(n, b, &digits), x % n == 0);
            }
        }
    }
}
