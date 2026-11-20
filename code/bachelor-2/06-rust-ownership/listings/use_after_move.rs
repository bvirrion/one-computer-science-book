// capture: exit
// use_after_move.rs: using a String after it moved.
fn main() {
    let a = String::from("Quay Street");
    let b = a;
    println!("{a} {b}");
}
