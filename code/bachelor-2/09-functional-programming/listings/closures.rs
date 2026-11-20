// closures.rs: closures capture by reference, by mutable reference, or by move.
fn apply_twice(f: impl Fn(u32) -> u32, x: u32) -> u32 {
    f(f(x))
}

fn make_fine(cents_per_day: u32, grace: u32) -> impl Fn(u32) -> u32 {
    // move: the closure owns its copies of the two numbers, and outlives this call
    move |days| days.saturating_sub(grace) * cents_per_day
}

fn main() {
    let rate = 10;
    let fine = |days: u32| days * rate; // borrows rate: Fn
    println!("{} {}", fine(4), apply_twice(fine, 3));

    let mut calls = 0;
    let mut count = || calls += 1; // borrows calls mutably: FnMut
    count();
    count();
    println!("calls {calls}");

    let title = String::from("Seven Comets");
    let give = move || title; // moves title in, and gives it away when called: FnOnce
    let t = give();
    println!("{t}");

    let fines: Vec<Box<dyn Fn(u32) -> u32>> =
        vec![Box::new(make_fine(10, 21)), Box::new(make_fine(25, 14))];
    println!("{:?}", fines.iter().map(|f| f(30)).collect::<Vec<_>>());
}
