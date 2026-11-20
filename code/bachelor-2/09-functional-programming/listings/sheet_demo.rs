// sheet_demo.rs: 100 cells, 1000 edits, every version kept.
mod sheet;
use sheet::{distinct_nodes, node_bytes, Cell, Sheet};
use std::rc::Rc;

fn main() {
    // cells 0..89: numbers, ten columns of nine rows; cells 90..99: the column totals
    let mut cells: Vec<(u32, Cell)> =
        (0..90).map(|k| (k, Cell::Num((k % 7) as f64))).collect();
    for c in 0..10 {
        let total: sheet::Formula =
            Rc::new(move |s: &Sheet| (0..9).map(|r| s.value(10 * r + c)).sum());
        cells.push((90 + c, Cell::Formula(total)));
    }
    let n = cells.len();
    let mut versions = vec![Sheet::new(&cells)];
    println!("{n} cells, formulas run: {}", versions[0].evaluations.get());
    println!("total of column 5 in version 0: {}", versions[0].value(95));
    for i in 0..1000u32 {
        let edited = versions.last().unwrap().set((i * 37) % 90, Cell::Num(i as f64));
        versions.push(edited);
    }
    let (first, last) = (&versions[0], versions.last().unwrap());
    println!("after 1000 edits: version 0 says {}, version 1000 {}",
             first.value(95), last.value(95));
    println!("formulas run: {}", last.evaluations.get());
    let k = versions.len() - 1;
    let depth = (n as f64).log2().ceil() as usize;
    let bound = n + k * (depth + 1);
    let nodes = distinct_nodes(&versions);
    println!("distinct nodes {nodes}, bound n + k(ceil(log2 n) + 1) = {bound}");
    println!("{} bytes per node; full copies would hold {} nodes", node_bytes(), (k + 1) * n);
}
