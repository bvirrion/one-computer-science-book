// ex11_family.rs -- exercise 11: grammars G_n of size O(n^2) whose LR(0)
// automaton has more than 2^n states. S -> X_i; X_i -> a_j X_i (j != i) | a_i.
#![allow(dead_code)]

pub fn family(n: usize) -> String {
    let mut s = String::from("S ->");
    for i in 1..=n {
        s += &format!("{} X{i}", if i == 1 { "" } else { " |" });
    }
    s += "\n";
    for i in 1..=n {
        s += &format!("X{i} -> a{i}");
        for j in (1..=n).filter(|&j| j != i) {
            s += &format!(" | a{j} X{i}");
        }
        s += "\n";
    }
    s
}
