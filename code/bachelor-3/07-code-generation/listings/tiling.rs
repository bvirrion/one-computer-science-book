// tiling.rs -- optimal instruction selection on an expression tree: each
// node's cheapest tiling, by dynamic programming from the leaves up.
use std::collections::HashMap;

enum N {
    Reg(&'static str),
    Const(i32),
    Addr(&'static str),
    Add(Box<N>, Box<N>),
    Mul(Box<N>, Box<N>),
    Load(Box<N>),
}
use N::*;

fn show(n: &N) -> String {
    match n {
        Reg(r) => r.to_string(),
        Const(c) => c.to_string(),
        Addr(g) => format!("&{g}"),
        Add(a, b) => format!("(+ {} {})", show(a), show(b)),
        Mul(a, b) => format!("(* {} {})", show(a), show(b)),
        Load(a) => format!("(mem {})", show(a)),
    }
}

fn imm(n: &N) -> Option<i32> {
    match n { Const(c) if (-2048..=2047).contains(c) => Some(*c), _ => None }
}
fn shift(n: &N) -> Option<u32> {
    match n {
        Const(c) if *c > 0 && (*c as u32).is_power_of_two() => Some(c.trailing_zeros()),
        _ => None,
    }
}

/// Every tile that matches at n: (instruction, its cost, the subtrees it leaves).
fn tiles(n: &N) -> Vec<(String, u32, Vec<&N>)> {
    let mut t = vec![];
    match n {
        Reg(_) => t.push(("(in a register)".into(), 0, vec![])),
        Const(c) => t.push((format!("li {c}"), 1, vec![])),
        Addr(g) => t.push((format!("la {g}"), 2, vec![])),
        Add(a, b) => {
            t.push(("add".into(), 1, vec![&**a, &**b]));
            if let Some(c) = imm(b) { t.push((format!("addi {c}"), 1, vec![&**a])); }
        }
        Mul(a, b) => {
            t.push(("mul".into(), 1, vec![&**a, &**b]));
            if let Some(k) = shift(b) { t.push((format!("slli {k}"), 1, vec![&**a])); }
        }
        Load(a) => {
            t.push(("lw 0(r)".into(), 1, vec![&**a]));
            if let Add(x, y) = &**a {
                if let Some(c) = imm(y) { t.push((format!("lw {c}(r)"), 1, vec![&**x])); }
            }
        }
    }
    t
}

/// Children first, then the node: its cost is the cheapest tile plus the
/// best costs, already known, of the subtrees that tile leaves.
fn best(n: &N, memo: &mut HashMap<*const N, u32>, naive: &mut u32) -> u32 {
    for k in children(n) {
        best(k, memo, naive);
    }
    let options: Vec<(String, u32)> = tiles(n).into_iter()
        .map(|(ins, c, kids)| {
            let below: u32 = kids.iter().map(|k| memo[&(*k as *const N)]).sum();
            (ins, c + below)
        })
        .collect();
    *naive += tiles(n)[0].1; // the first tile covers this node alone
    let (ins, cost) = options.into_iter().min_by_key(|o| o.1).unwrap();
    println!("{:<40} {:<16} {cost:>2}", show(n), ins);
    memo.insert(n as *const N, cost);
    cost
}

fn children(n: &N) -> Vec<&N> {
    match n { Add(a, b) | Mul(a, b) => vec![a, b], Load(a) => vec![a], _ => vec![] }
}

fn main() {
    // sq[i + 1] * 4 + 7, the address of sq[i + 1] written as &sq + i*4 + 4
    let b = Box::new;
    let addr = Add(b(Add(b(Addr("sq")), b(Mul(b(Reg("i")), b(Const(4)))))), b(Const(4)));
    let tree = Add(b(Mul(b(Load(b(addr))), b(Const(4)))), b(Const(7)));
    println!("{:<40} {:<16} {}", "subtree", "best tile", "cost");
    let mut naive = 0;
    let opt = best(&tree, &mut HashMap::new(), &mut naive);
    println!("optimal: {opt} instructions; one tile per node: {naive}");
}
