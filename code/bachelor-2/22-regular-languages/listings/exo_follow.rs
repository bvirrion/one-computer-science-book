// exo_follow.rs: the Glushkov sets of a(ba|b)*a (exercise 5).
#[allow(dead_code)]
mod regex;

fn main() {
    let g = regex::glushkov(&regex::parse("a(ba|b)*a").unwrap());
    let numbered: Vec<String> = g.letters.iter().enumerate()
        .map(|(j, c)| format!("{c}{}", j + 1)).collect();
    println!("{}; nullable {}; first {:?}; last {:?}", numbered.join(" "), g.nullable,
             g.first, g.last);
    for j in 1..=g.letters.len() {
        println!("follow({j}) = {:?}", g.follow[j]);
    }
}
