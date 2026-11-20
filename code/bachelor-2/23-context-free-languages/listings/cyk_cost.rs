// cyk_cost.rs: CYK on longer and longer documents: split points counted, and time.
#[allow(dead_code)]
mod grammar;
use std::time::Instant;

fn main() {
    let g = grammar::Grammar::parse("D -> I D | I\nI -> w | < D > | [ D ]").cnf();
    println!("   n  accepted  split points  (n^3 - n)/6  time (ms)");
    for k in [3, 6, 12, 24, 48] {
        let doc = "<w[w]w>".repeat(k); // 7 letters each time
        let n = doc.len();
        let t = Instant::now();
        let (table, splits) = g.cyk(&doc);
        let ms = t.elapsed().as_secs_f64() * 1e3;
        let ok = table[0][n - 1].contains(&g.start);
        println!("{n:4}  {ok:8}  {splits:12}  {:11}  {ms:9.1}", (n * n * n - n) / 6);
    }
}
