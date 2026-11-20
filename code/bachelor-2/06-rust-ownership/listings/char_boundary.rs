// capture: exit
// char_boundary.rs: a byte index that falls inside a character.
fn main() {
    // print a panic as the default does, without the thread's number, which changes at each run
    std::panic::set_hook(Box::new(|p| {
        eprintln!("panicked at {}:\n{}", p.location().unwrap(), p.payload_as_str().unwrap_or("?"))
    }));
    let street = String::from("Café Lane");
    let n: usize = std::env::args().count() + 3; // 4, from a value only known at run time
    println!("first {n} bytes: {}", &street[0..n]);
}
