//! Tests of chapter 23: CYK on the Chomsky normal form against the generated words, tree
//! counts, the grammar's pushdown automaton, leftmost derivations, the recogniser.
#[allow(dead_code)]
#[path = "../../../listings/grammar.rs"]
pub mod grammar;
#[allow(dead_code)]
#[path = "../../../listings/count.rs"]
pub mod count;
#[allow(dead_code)]
#[path = "../../../listings/pda.rs"]
pub mod pda;
#[path = "../../../exercises/bigcount.rs"]
pub mod bigcount;
#[path = "../../../exercises/descent.rs"]
pub mod descent;

#[cfg(test)]
mod tests {
    use super::grammar::{Grammar, Sym};
    use super::*;

    const GRAMMARS: [&str; 9] = [
        "E -> E + T | T\nT -> T * F | F\nF -> ( E ) | a",
        "E -> E + E | E * E | ( E ) | a",
        "S -> ( S ) S | ε",
        "P -> a P a | b P b | a | b | ε",
        "D -> I D | I\nI -> w | < D > | [ D ]",
        "S -> i S | i S e S | x",
        "S -> a S b | ε",
        "S -> A | a b\nA -> B | a\nB -> A | b",
        "S -> A S A | a B\nA -> B | S\nB -> b | ε",
    ];

    /// Every word over the given letters, up to length n.
    fn all_words(letters: &[char], n: usize) -> Vec<String> {
        let (mut words, mut layer) = (vec![String::new()], vec![String::new()]);
        for _ in 0..n {
            layer = layer.iter().flat_map(|w| letters.iter().map(move |c| format!("{w}{c}")))
                .collect();
            words.extend(layer.iter().cloned());
        }
        words
    }

    fn letters(g: &Grammar) -> Vec<char> {
        let mut out: Vec<char> = g.rules.iter().flat_map(|(_, r)| r.iter())
            .filter_map(|s| if let Sym::T(c) = s { Some(*c) } else { None }).collect();
        out.sort();
        out.dedup();
        out
    }

    #[test]
    fn cnf_and_cyk_agree_with_the_generated_words() {
        for text in GRAMMARS {
            let g = Grammar::parse(text);
            let c = g.cnf();
            for (_, rhs) in &c.rules { // the shape of a Chomsky normal form
                let ok = matches!(rhs.as_slice(), [Sym::T(_)] | [Sym::N(_), Sym::N(_)] | []);
                assert!(ok, "{text}: {}", grammar::show(rhs));
            }
            let n = if letters(&g).len() > 4 { 6 } else { 8 };
            let made = g.generated(n);
            for w in all_words(&letters(&g), n) {
                assert_eq!(c.accepts(&w), made.contains(&w), "{text} on {w:?}");
            }
        }
    }

    #[test]
    fn splits_are_cubic() {
        let c = Grammar::parse(GRAMMARS[4]).cnf();
        for n in 1..30 {
            let (_, splits) = c.cyk(&"w".repeat(n));
            assert_eq!(splits, (n * n * n - n) / 6);
        }
    }

    #[test]
    fn tree_counts() {
        let g = Grammar::parse("E -> E + E | a");
        let c = g.cnf();
        let mut catalan: u128 = 1;
        for k in 1..=15u128 {
            let w = vec!["a"; k as usize].join("+");
            assert_eq!(count::trees(&g, &w), catalan);
            assert_eq!(bigcount::trees(&c, &w).decimal(), catalan.to_string());
            catalan = catalan * 2 * (2 * k - 1) / (k + 1);
        }
        let unambiguous = Grammar::parse(GRAMMARS[0]);
        for w in unambiguous.generated(7) {
            assert_eq!(count::trees(&unambiguous, &w), 1, "{w}");
        }
        let big = bigcount::Big::small(4_000_000_000).mul(&bigcount::Big::small(4_000_000_000));
        assert_eq!(big.decimal(), "16000000000000000000");
    }

    #[test]
    fn grammar_automaton_and_derivations() {
        for text in [GRAMMARS[2], GRAMMARS[3], GRAMMARS[6]] {
            let g = Grammar::parse(text);
            let m = pda::Pda::from_grammar(&g);
            let made = g.generated(8);
            for w in all_words(&letters(&g), 8) {
                assert_eq!(m.accepts(&w, 2 * w.len() + 4).0, made.contains(&w), "{text} {w}");
            }
            for w in g.generated(6) {
                let steps = g.leftmost(&w).expect("a derivation");
                for pair in steps.windows(2) { // one rule, applied at the leftmost nonterminal
                    let k = pair[0].iter().position(|s| matches!(s, Sym::N(_))).unwrap();
                    let applied = g.rules.iter().any(|(a, rhs)| {
                        pair[0][k] == Sym::N(a.clone())
                            && pair[1] == [&pair[0][..k], rhs, &pair[0][k + 1..]].concat()
                    });
                    assert!(applied, "{text}: {w}");
                }
            }
        }
    }

    #[test]
    fn hand_written_recogniser() {
        let g = Grammar::parse("S -> T S | c\nT -> a S b");
        let made = g.generated(10);
        for w in all_words(&['a', 'b', 'c'], 10) {
            assert_eq!(descent::recognise(&w), made.contains(&w), "{w}");
        }
    }
}
