// exo_decimal.rs: an expression for chapter 21's decimal numbers, checked against its DFA
// on every string of length at most 6 over 0 1 + - . e E (exercise 3).
#[allow(dead_code)]
mod regex;
#[allow(dead_code)]
#[path = "../../21-finite-automata/listings/dfa_demo.rs"]
mod dfa_demo;

fn main() {
    let text = "[+-]?[0-9]+(.[0-9]+)?([eE][+-]?[0-9]+)?";
    let m = regex::Matcher::new(&regex::glushkov(&regex::parse(text).unwrap()));
    let alphabet = ['0', '1', '+', '-', '.', 'e', 'E'];
    let (mut words, mut layer) = (vec![String::new()], vec![String::new()]);
    for _ in 0..6 {
        layer = layer.iter().flat_map(|w| alphabet.iter().map(move |c| format!("{w}{c}")))
            .collect();
        words.extend(layer.iter().cloned());
    }
    let differ: Vec<&String> = words.iter()
        .filter(|w| m.matches(w) != dfa_demo::is_number(w).0).collect();
    let accepted = words.iter().filter(|w| m.matches(w)).count();
    println!("{} strings, {accepted} numbers, {} disagreements", words.len(), differ.len());
}
