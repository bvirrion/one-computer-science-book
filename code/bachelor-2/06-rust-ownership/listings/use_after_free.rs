// capture: exit
// use_after_free.rs: the same program in Rust.
fn main() {
    let name = String::from("Mill Lane");
    let shown = &name; // a reference to the same string
    drop(name); // the owner gives the string back
    println!("{shown}"); // ...and the reference still uses it
}
