// dfa_table.rs -- the scanner DFA of four token rules, as a table.
#[path = "regex_nfa.rs"]
mod regex_nfa;
#[path = "scanner_dfa.rs"]
mod scanner_dfa;
use scanner_dfa::DEAD;

const RULES: [(&str, &str); 4] =
    [("if", "if"), ("ident", "[a-z][a-z0-9]*"), ("number", "[0-9]+"), ("space", "[ \\n]+")];

fn show(c: u8) -> String {
    match c {
        b' ' => "' '".into(),
        b'\n' => "\\n".into(),
        _ => (c as char).to_string(),
    }
}

fn main() {
    let regexes: Vec<&str> = RULES.iter().map(|r| r.1).collect();
    let nfa = regex_nfa::union(&regexes).unwrap();
    let big = scanner_dfa::subset(&nfa);
    let dfa = scanner_dfa::minimise(&big);
    println!("NFA {} states, DFA {} states, minimal {}", nfa.states.len(), big.next.len(), dfa.next.len());
    for (s, row) in dfa.next.iter().enumerate() {
        let class = dfa.accept[s].map_or("-", |r| RULES[r].0);
        let mut moves = Vec::new();
        let mut c = 0;
        while c < 128 {
            let t = row[c];
            let mut e = c;
            while e + 1 < 128 && row[e + 1] == t {
                e += 1;
            }
            if t != DEAD {
                let (a, b) = (show(c as u8), show(e as u8));
                moves.push(if c == e { format!("{a}->{t}") } else { format!("{a}-{b}->{t}") });
            }
            c = e + 1;
        }
        println!("state {s}  accepts {class:<7} {}", moves.join("  "));
    }
}
