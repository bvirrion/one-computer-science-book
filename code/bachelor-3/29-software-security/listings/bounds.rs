// capture: exit
// bounds.rs -- the login desk's copy in Rust. Copying into a slice of the buffer is
// checked: a name longer than the buffer stops the program with a panic, and no
// byte outside the buffer is ever written.
use std::io::{self, BufRead, Write};

fn check(typed: &str) -> bool {
    let is_admin = false;
    let mut name = [0u8; 16];
    name[..typed.len()].copy_from_slice(typed.as_bytes()); // checked: panics if too long
    println!("hello {}", String::from_utf8_lossy(&name[..typed.len()]));
    is_admin
}

fn main() {
    // print a panic as the default does, without the thread's number, which changes at each run
    std::panic::set_hook(Box::new(|p| {
        eprintln!("panicked at {}:\n{}", p.location().unwrap(), p.payload_as_str().unwrap_or("?"))
    }));
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        print!("{:2} bytes typed: ", line.len());
        io::stdout().flush().unwrap();
        println!("{}", if check(&line) { "admin desk opened" } else { "reader desk" });
    }
}
