// capture: exit
// fn_once_error.rs: a closure that gives away what it captured can run only once.
fn main() {
    let title = String::from("Seven Comets");
    let give = move || title;
    let a = give();
    let b = give();
    println!("{a} {b}");
}
