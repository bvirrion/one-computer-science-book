// glushkov.rs: the positions of (a|b)*abb, their first, last and follow sets, the automaton.
#[allow(dead_code)]
mod regex;

fn main() {
    let re = regex::parse("(a|b)*abb").unwrap();
    let g = regex::glushkov(&re);
    let numbered: Vec<String> = g.letters.iter().enumerate()
        .map(|(j, c)| format!("{c}{}", j + 1)).collect();
    println!("positions: {}   nullable: {}", numbered.join(" "), g.nullable);
    println!("first: {:?}   last: {:?}", g.first, g.last);
    for j in 1..=g.letters.len() {
        println!("follow({j}) = {:?}", g.follow[j]);
    }
    let m = regex::Matcher::new(&g);
    let words = regex::lang(&regex::parse("(a|b)*").unwrap(), 8);
    let agree = words.iter().filter(|w| m.matches(w) == regex::lang(&re, 8).contains(*w))
        .count();
    println!("{agree} of {} words up to length 8 judged as the definition says", words.len());
}
