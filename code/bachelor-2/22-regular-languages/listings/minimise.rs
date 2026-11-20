// minimise.rs: Moore's refinement on the DFA of a(a|b)*|b(a|b)*b|b.
#[allow(dead_code)]
mod dfa;
#[allow(dead_code)]
mod regex;

fn main() {
    let re = regex::parse("a(a|b)*|b(a|b)*b|b").unwrap();
    let d = dfa::determinise(&regex::glushkov(&re), &['a', 'b']);
    println!("state  on a  on b  accepting");
    for (q, row) in d.delta.iter().enumerate() {
        println!("{q:5} {:5} {:5}  {}", row[0], row[1], d.accept[q]);
    }
    for (i, class) in dfa::moore(&d).iter().enumerate() {
        println!("round {i}: classes {class:?}");
    }
    let m = dfa::minimise(&d);
    println!("minimal automaton: {} states, from {}", m.delta.len(), d.delta.len());
}
