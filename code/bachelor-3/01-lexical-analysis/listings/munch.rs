// munch.rs -- how many characters maximal munch reads on a^n
// when the rules are `a` and `a*b`.
#[path = "regex_nfa.rs"]
mod regex_nfa;
#[path = "scanner_dfa.rs"]
mod scanner_dfa;

fn main() {
    let nfa = regex_nfa::union(&["a", "a*b"]).unwrap();
    let dfa = scanner_dfa::minimise(&scanner_dfa::subset(&nfa));
    println!("{:>6} {:>7} {:>10} {:>10}", "n", "tokens", "reads", "n(n+1)/2");
    for n in [1, 2, 5, 10, 100, 1000, 10000] {
        let input = vec![b'a'; n];
        let (tokens, reads) = scanner_dfa::scan(&dfa, &input).unwrap();
        println!("{:>6} {:>7} {:>10} {:>10}", n, tokens.len(), reads, n * (n + 1) / 2);
    }
    let mut ab = vec![b'a'; 10000];
    ab.push(b'b');
    let (tokens, reads) = scanner_dfa::scan(&dfa, &ab).unwrap();
    println!("a^10000 b: {} token, {} reads", tokens.len(), reads);
}
