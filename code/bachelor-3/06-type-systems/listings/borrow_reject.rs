// borrow_reject.rs -- a value used after it was moved: the borrow checker
// rejects the program, as a type checker rejects a type error.
// capture: exit
fn total(v: Vec<i32>) -> i32 {
    v.iter().sum()
}

fn main() {
    let v = vec![1, 2, 3];
    let t = total(v); // v is moved into total
    println!("{t} {}", v.len()); // used again: rejected
}
