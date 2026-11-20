//! Tests of chapter 22: the engine against the denotation, canonical minimisation,
//! state elimination round trips, Hopcroft against Moore, equivalence.
#[allow(dead_code)]
#[path = "../../../listings/regex.rs"]
pub mod regex;
#[allow(dead_code)]
#[path = "../../../listings/dfa.rs"]
pub mod dfa;
#[path = "../../../exercises/hopcroft.rs"]
pub mod hopcroft;

#[cfg(test)]
mod tests {
    use super::dfa::{determinise, difference, eliminate, minimise, moore, Dfa};
    use super::hopcroft::hopcroft;
    use super::regex::*;

    const SAMPLES: [&str; 14] = [
        "(a|b)*abb", "a*b*", "(ab|b)*a?", "((a|b)(a|b))*", "(a|ε)(b|ε)", "a(ba|b)*a",
        "(aa|a)*", "a{2,4}b?", "[ab]+a", "ε", "(a*|b)*", "b(a|b){3}", "(ab)*|(ba)*", "a|b|ab",
    ];

    fn all_words(n: usize) -> std::collections::BTreeSet<String> {
        lang(&parse("(a|b)*").unwrap(), n)
    }

    #[test]
    fn engine_matches_denotation() {
        let words = all_words(8);
        for text in SAMPLES {
            let re = parse(text).unwrap();
            let l = lang(&re, 8);
            let m = Matcher::new(&glushkov(&re));
            let d = determinise(&glushkov(&re), &['a', 'b']);
            for w in &words {
                assert_eq!(m.matches(w), l.contains(w), "{text} on {w}");
                assert_eq!(d.accepts(w), l.contains(w), "{text} (DFA) on {w}");
            }
            let (_, steps) = m.run("abababab");
            assert!(steps <= (glushkov(&re).letters.len() + 1) * 8);
        }
    }

    #[test]
    fn parse_errors() {
        for bad in ["(a", "a)", "*a", "a|*", "[]", "a{2"] {
            assert!(parse(bad).is_err(), "{bad}");
        }
        assert_eq!(parse("[a-c]").unwrap().show(), "a|b|c");
    }

    /// Two minimal automata of the same language are equal up to renumbering: compare
    /// them by a joint walk that builds the bijection.
    fn isomorphic(x: &Dfa, y: &Dfa) -> bool {
        if x.delta.len() != y.delta.len() {
            return false;
        }
        let mut map = vec![usize::MAX; x.delta.len()];
        let mut todo = vec![(0, 0)];
        map[0] = 0;
        while let Some((p, q)) = todo.pop() {
            if x.accept[p] != y.accept[q] {
                return false;
            }
            for a in 0..x.alphabet.len() {
                let (r, s) = (x.delta[p][a], y.delta[q][a]);
                if map[r] == usize::MAX {
                    map[r] = s;
                    todo.push((r, s));
                } else if map[r] != s {
                    return false;
                }
            }
        }
        true
    }

    #[test]
    fn minimisation_is_canonical() {
        let pairs = [("(a|b)*", "(a*b*)*"), ("(ab)*a", "a(ba)*"), ("(aa|a)*", "a*"),
                     ("a(a|b)*|b(a|b)*b|b", "a(a|b)*|b((a|b)*b)?")];
        let auto = |t: &str| determinise(&glushkov(&parse(t).unwrap()), &['a', 'b']);
        for (x, y) in pairs {
            assert!(difference(&auto(x), &auto(y)).is_none(), "{x} vs {y}");
            assert!(isomorphic(&minimise(&auto(x)), &minimise(&auto(y))), "{x} vs {y}");
        }
        for text in SAMPLES {
            let d = auto(text);
            assert_eq!(&hopcroft(&d), moore(&d).last().unwrap(), "{text}");
            let m = minimise(&d);
            assert!(difference(&d, &m).is_none());
            assert_eq!(minimise(&m).delta.len(), m.delta.len()); // already minimal
        }
        assert_eq!(difference(&auto("a*b*"), &auto("(a|b)*")), Some("ba".to_string()));
    }

    #[test]
    fn elimination_round_trip() {
        for text in SAMPLES {
            let d = determinise(&glushkov(&parse(text).unwrap()), &['a', 'b']);
            let back = eliminate(&d);
            let again = determinise(&glushkov(&back), &['a', 'b']);
            assert!(difference(&d, &again).is_none(), "{text} -> {}", back.show());
        }
    }
}
