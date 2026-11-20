// cyk.rs: the CYK table of a+a*a for the grammar of cnf.rs.
#[allow(dead_code)]
mod grammar;

fn main() {
    let g = grammar::Grammar::parse("E -> E + T | T\nT -> T * F | F\nF -> ( E ) | a").cnf();
    let word = "a+a*a";
    let (table, splits) = g.cyk(word);
    for l in (1..=word.len()).rev() { // the longest spans on top, as in a pyramid
        let row: Vec<String> = (0..=word.len() - l).map(|i| {
            let cell: Vec<&str> = table[i][l - 1].iter().map(|s| s.as_str()).collect();
            format!("{{{}}}", cell.join(","))
        }).collect();
        println!("length {l}: {}", row.join(" "));
    }
    let accepted = table[0][word.len() - 1].contains(&g.start);
    println!("{word} accepted: {accepted}; split points tried: {splits}");
}
