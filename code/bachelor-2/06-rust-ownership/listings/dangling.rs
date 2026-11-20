// capture: exit
// dangling.rs: a function that returns a reference to its own local string.
fn default_street() -> &String {
    let s = String::from("Mill Lane");
    &s
}

fn main() {
    println!("{}", default_street());
}
