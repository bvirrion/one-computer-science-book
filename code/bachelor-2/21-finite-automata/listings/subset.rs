// subset.rs: the subset construction on "the 3rd letter from the end is a".
#[allow(dead_code)]
mod automaton;
use automaton::{kth_from_end, Subset};

fn show(s: &Subset) -> String {
    let inner: Vec<String> = s.iter().map(|q| q.to_string()).collect();
    format!("{{{}}}", inner.join(","))
}

fn main() {
    let nfa = kth_from_end(3);
    let (dfa, subsets) = nfa.determinise();
    println!("DFA state  subset of NFA states   on a       on b");
    for (i, s) in subsets.iter().enumerate() {
        let [a, b] = [0, 1].map(|x| show(&subsets[dfa.delta[i][x].unwrap()]));
        let mark = if dfa.accept[i] { "accepting" } else { "" };
        let line = format!("{i:9}  {:20}  {a:9}  {b:9}  {mark}", show(s));
        println!("{}", line.trim_end());
    }
    for w in ["abb", "bab", "baab", "abba"] {
        println!("{w:6} NFA {:5}  DFA {}", nfa.accepts(w), dfa.accepts(w));
    }
}
