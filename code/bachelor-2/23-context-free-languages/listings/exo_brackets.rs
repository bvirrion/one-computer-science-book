// exo_brackets.rs: a grammar meant for balanced brackets, and its words (exercise 2).
#[allow(dead_code)]
mod grammar;

fn balanced(w: &str) -> bool {
    let mut depth = 0i32;
    w.chars().all(|c| {
        depth += if c == '(' { 1 } else { -1 };
        depth >= 0
    }) && depth == 0
}

fn main() {
    let g = grammar::Grammar::parse("S -> ( S ) S | ) S ( S | ε");
    for w in g.generated(4).iter().filter(|w| !w.is_empty()) {
        println!("{w:5} balanced: {}", balanced(w));
    }
    let equal = |w: &String| w.matches('(').count() == w.matches(')').count();
    let all = g.generated(10).iter().all(equal);
    println!("every word up to length 10 has as many ( as ): {all}");
}
