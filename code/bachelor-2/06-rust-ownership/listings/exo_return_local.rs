// capture: exit
// exo_return_local.rs: the names joined into one line, returned as a string slice.
fn joined(names: &[String]) -> &str {
    let line = names.join(", ");
    &line
}

fn main() {
    let names = vec![String::from("Mill Row"), String::from("Quay Street")];
    println!("{}", joined(&names));
}
