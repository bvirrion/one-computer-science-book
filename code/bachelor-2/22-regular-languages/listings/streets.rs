// streets.rs: patterns over the town's street names.
#[allow(dead_code)]
mod regex;

fn main() {
    let table = std::fs::read_to_string("../../../../data/town/streets.csv").unwrap();
    let names: Vec<&str> = table.lines().skip(1)
        .map(|line| line.split(',').nth(1).unwrap()).collect();
    let patterns = ["[A-Z][a-z]* Road", "[A-Z][a-z]* (Road|Row|Way)",
                    "(Mill|River) [A-Za-z]*", "[A-Z][a-z]*(e|n) [A-Z][a-z]*",
                    "[A-Z][a-z]* [A-Z][a-z]*"];
    for pattern in patterns {
        let re = regex::parse(pattern).unwrap();
        let g = regex::glushkov(&re);
        let m = regex::Matcher::new(&g);
        let hits: Vec<&str> = names.iter().copied().filter(|n| m.matches(n)).collect();
        let some = hits.iter().take(2).copied().collect::<Vec<_>>().join(", ");
        let (m, k) = (g.letters.len(), hits.len());
        println!("{pattern:31} {m:3} positions {k:3} of {}: {some}", names.len());
    }
}
