// exo_sizes.rs: how big is a closure? Predict the three numbers.
use std::mem::size_of_val;

fn main() {
    let rate: u32 = 10;
    let title = String::from("Seven Comets");
    let pages: [u64; 4] = [65, 133, 412, 98];

    let a = |d: u32| d * 2;                       // captures nothing
    let b = |d: u32| d * rate + title.len() as u32; // captures rate and title by reference
    let c = move |i: usize| pages[i] + rate as u64; // moves pages and rate in
    println!("{} {} {}", size_of_val(&a), size_of_val(&b), size_of_val(&c));
    println!("{} {} {}", a(1), b(1), c(1));
}
