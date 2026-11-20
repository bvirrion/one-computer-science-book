// move_string.rs: assignment moves a String, copies an integer, and clone copies on request.
fn main() {
    let a = String::from("Quay Street");
    let b = a; // a move: b now owns the buffer; a can no longer be used
    let c = b.clone(); // a second buffer, with the same bytes
    println!("b = {b}, c = {c}");
    println!("same buffer? {}", b.as_ptr() == c.as_ptr());

    let x = 42; // an i32 is Copy: assignment copies the bits
    let y = x;
    println!("x = {x}, y = {y}"); // both usable

    let moved_into = takes(c); // c moves into the function's parameter...
    println!("{moved_into}"); // ...and the result moves back out
}

fn takes(s: String) -> usize {
    s.len()
} // s is dropped here: its buffer is freed
