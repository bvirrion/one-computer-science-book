// markup.rs: the town's markup: a first grammar, its ambiguity, a second grammar, its CNF.
// Letters: w a word, * around bold text in the first version, < > in the second, [ ] a link.
#[allow(dead_code)]
mod count;
#[allow(dead_code)]
mod grammar;
use grammar::Grammar;

fn main() {
    let first = Grammar::parse("D -> D D | w | * D * | [ D ]");
    println!("{}", first.show());
    for doc in ["w", "ww", "www", "[w]w[w]", "*w*w*w*", "**w**"] {
        println!("  {doc:10} {} trees", count::trees(&first, doc));
    }
    let second = Grammar::parse("D -> I D | I\nI -> w | < D > | [ D ]");
    println!("{}", second.show());
    let docs = second.generated(8);
    let unique = docs.iter().all(|d| count::trees(&second, d) == 1);
    println!("  each of the {} documents up to length 8 has one tree: {unique}", docs.len());
    let c = second.cnf();
    println!("in Chomsky normal form ({} rules):\n{}", c.rules.len(), c.show());
    for doc in ["<w[w]>w", "<w[w>]w", "[<ww>]"] {
        let (table, splits) = c.cyk(doc);
        let ok = table[0][doc.len() - 1].contains(&c.start);
        println!("  {doc:8} accepted: {ok:5}  split points: {splits}");
        for l in (1..=doc.len()).rev().filter(|_| doc == "<w[w]>w") { // the first one's table
            let row: Vec<String> = (0..=doc.len() - l).map(|i| {
                let cell: Vec<&str> = table[i][l - 1].iter().map(|s| s.as_str()).collect();
                format!("{{{}}}", cell.join(","))
            }).collect();
            println!("    length {l}: {}", row.join(" "));
        }
    }
}
