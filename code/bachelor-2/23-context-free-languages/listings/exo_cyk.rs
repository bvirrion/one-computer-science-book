// exo_cyk.rs: the CYK table of aabb for S -> A B | A C, C -> S B, A -> a, B -> b
// (exercise 5).
#[allow(dead_code)]
mod grammar;

fn main() {
    let g = grammar::Grammar::parse("S -> A B | A C\nC -> S B\nA -> a\nB -> b");
    for word in ["aabb", "abab"] {
        let (table, _) = g.cyk(word);
        println!("{word}:");
        for l in (1..=4).rev() {
            let row: Vec<String> = (0..=4 - l).map(|i| {
                let cell: Vec<&str> = table[i][l - 1].iter().map(|s| s.as_str()).collect();
                format!("{{{}}}", cell.join(","))
            }).collect();
            println!("  length {l}: {}", row.join(" "));
        }
    }
}
