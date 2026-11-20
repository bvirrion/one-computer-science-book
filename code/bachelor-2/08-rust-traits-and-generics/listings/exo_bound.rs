// capture: exit
// exo_bound.rs: print every item, then the number of distinct ones.
use std::collections::HashSet;

fn report<T>(items: &[T]) {
    for x in items {
        println!("{x}");
    }
    let distinct: HashSet<&T> = items.iter().collect();
    println!("{} distinct", distinct.len());
}

fn main() {
    report(&["Mill Lane", "Quay Street", "Mill Lane"]);
}
