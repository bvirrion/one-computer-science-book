// capture: exit
// two_mut.rs: two exclusive borrows of one String at the same time.
fn main() {
    let mut street = String::from("Mill");
    let first = &mut street;
    let second = &mut street;
    first.push_str(" Lane");
    second.push_str(" Row");
    println!("{street}");
}
