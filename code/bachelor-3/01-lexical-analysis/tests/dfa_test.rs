// Tests of Thompson's construction, the subset construction with priorities,
// minimisation and maximal munch; the generated scanner is checked against
// the hand-written one on generated inputs.
#[path = "../listings/lexer.rs"]
mod lexer;
#[path = "../exercises/memo_munch.rs"]
mod memo_munch;
#[path = "../listings/regex_nfa.rs"]
mod regex_nfa;
#[path = "../listings/scanner_dfa.rs"]
mod scanner_dfa;
#[path = "../listings/token.rs"]
mod token;

fn states(re: &str) -> usize {
    regex_nfa::union(&[re]).unwrap().states.len() - 1 // without the union's start
}

#[test]
fn thompson_counts_two_states_per_symbol_and_operator() {
    assert_eq!(states("a"), 2);
    assert_eq!(states("if"), 4);
    assert_eq!(states("[a-z][a-z0-9]*"), 6);
    assert_eq!(states("(a|b)*abb"), 14); // exercise 4
    assert_eq!(states("//[^\\n]*"), 8);
    assert_eq!(states("[0-9]+(\\.[0-9]+)?"), 12);
}

#[test]
fn exercise_9_keywords_as_rules_cost_states() {
    let ident = "[A-Za-z_][A-Za-z0-9_]*";
    let alone = dfa(&[ident]).next.len();
    let mut rules: Vec<&str> = KEYWORDS.to_vec();
    rules.push(ident);
    let with = dfa(&rules).next.len();
    assert_eq!((alone, with), (2, 43));
}

fn dfa(rules: &[&str]) -> scanner_dfa::Dfa {
    scanner_dfa::minimise(&scanner_dfa::subset(&regex_nfa::union(rules).unwrap()))
}

fn accepts(d: &scanner_dfa::Dfa, s: &str) -> Option<usize> {
    let mut q = 0;
    for c in s.bytes() {
        q = d.next[q][c as usize];
        if q == scanner_dfa::DEAD {
            return None;
        }
    }
    d.accept[q]
}

#[test]
fn the_first_rule_wins_a_tie() {
    let d = dfa(&["if", "[a-z]+"]);
    assert_eq!(accepts(&d, "if"), Some(0));
    assert_eq!(accepts(&d, "iffy"), Some(1));
    let swapped = dfa(&["[a-z]+", "if"]);
    assert_eq!(accepts(&swapped, "if"), Some(0)); // the keyword is unreachable
}

#[test]
fn table_sizes_printed_in_the_chapter() {
    let rules = ["if", "[a-z][a-z0-9]*", "[0-9]+", "[ \\n]+"];
    let nfa = regex_nfa::union(&rules).unwrap();
    let big = scanner_dfa::subset(&nfa);
    assert_eq!((nfa.states.len(), big.next.len(), scanner_dfa::minimise(&big).next.len()), (19, 7, 6));
}

// Moor's token rules, keywords first (the priority rule does the rest).
const KEYWORDS: [&str; 11] = ["fn", "var", "array", "if", "else", "while", "return", "true", "false", "int", "bool"];
const OPS: [&str; 25] = ["\\+", "-", "\\*", "/", "%", "==", "!=", "<", "<=", ">", ">=", "&&", "\\|\\|", "!", "=",
    "\\(", "\\)", "{", "}", "\\[", "\\]", ",", ";", ":", "->"];

fn moor_rules() -> Vec<String> {
    let mut r: Vec<String> = KEYWORDS.iter().map(|s| s.to_string()).collect();
    r.push("[A-Za-z_][A-Za-z0-9_]*".into());
    r.push("[0-9]+".into());
    r.extend(OPS.iter().map(|s| s.to_string()));
    r.push("[ \\t\\n\\r]+".into());
    r.push("//[^\\n]*".into());
    r
}

#[test]
fn the_generated_scanner_agrees_with_the_hand_written_one() {
    let rules = moor_rules();
    let refs: Vec<&str> = rules.iter().map(|s| s.as_str()).collect();
    let d = dfa(&refs);
    let pool = ["if", "iffy", "x1", "42", " ", "\n", "<", "=", "<=", "-", ">", "->", "&&", "||", "!",
        "// c\n", "while", "_", "(", ")", "{", "}", ";", "a", "7", "!="];
    let mut seed: u64 = 1;
    for _ in 0..2000 {
        let mut src = String::new();
        for _ in 0..12 {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            src.push_str(pool[(seed >> 33) as usize % pool.len()]);
        }
        let hand: Vec<String> = lexer::lex(&src).unwrap().iter()
            .filter(|t| t.kind != token::TokenKind::Eof)
            .map(|t| src[t.span.start..t.span.end].to_string()).collect();
        let (gen, _) = scanner_dfa::scan(&d, src.as_bytes()).unwrap();
        let gen: Vec<String> = gen.iter()
            .filter(|(r, _, _)| *r < rules.len() - 2) // drop white space and comments
            .map(|&(_, a, b)| src[a..b].to_string()).collect();
        assert_eq!(hand, gen, "on {src:?}");
    }
}

#[test]
fn naive_munch_is_quadratic_and_memo_munch_linear() {
    let d = dfa(&["a", "a*b"]);
    for n in [2usize, 10, 100, 1000] {
        let input = vec![b'a'; n];
        let (t1, naive) = scanner_dfa::scan(&d, &input).unwrap();
        let (t2, memo) = memo_munch::scan_memo(&d, &input).unwrap();
        assert_eq!(t1, t2);
        assert_eq!(naive, n * (n + 1) / 2);
        assert_eq!(memo, 3 * n - 3);
    }
}

#[test]
fn memo_munch_gives_the_same_tokens() {
    let rules = moor_rules();
    let refs: Vec<&str> = rules.iter().map(|s| s.as_str()).collect();
    let d = dfa(&refs);
    let src = std::fs::read_to_string("../listings/hello.moor").unwrap();
    let (a, _) = scanner_dfa::scan(&d, src.as_bytes()).unwrap();
    let (b, _) = memo_munch::scan_memo(&d, src.as_bytes()).unwrap();
    assert_eq!(a, b);
}
