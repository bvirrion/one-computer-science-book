// pb_timetable.rs -- the weekend problem: a scanner for the town hall's
// timetables, its tables, and what maximal munch costs on a rule line.
#![allow(dead_code)]
use crate::regex_nfa;
use crate::scanner_dfa::{self, Dfa};

pub const RULES: [(&str, &str); 7] = [
    ("time", "[0-9][0-9]:[0-9][0-9]"),
    ("number", "[0-9]+"),
    ("name", "[A-Z][a-z]*"),
    ("word", "[a-z]+"),
    ("arrow", "-+>"),
    ("dash", "-"),
    ("space", "[ \\n]+"),
];

pub fn build() -> (usize, usize, Dfa) {
    let regexes: Vec<&str> = RULES.iter().map(|r| r.1).collect();
    let nfa = regex_nfa::union(&regexes).unwrap();
    let big = scanner_dfa::subset(&nfa);
    let n_big = big.next.len();
    (nfa.states.len(), n_big, scanner_dfa::minimise(&big))
}

/// Columns of the table that are identical: the character classes.
pub fn char_classes(d: &Dfa) -> usize {
    let mut cols: Vec<Vec<usize>> = (0..128).map(|c| d.next.iter().map(|row| row[c]).collect()).collect();
    cols.sort();
    cols.dedup();
    cols.len()
}

pub fn tokens(d: &Dfa, s: &str) -> Vec<(String, String)> {
    let (toks, _) = scanner_dfa::scan(d, s.as_bytes()).unwrap();
    toks.iter().map(|&(r, a, b)| (RULES[r].0.to_string(), s[a..b].to_string())).collect()
}
