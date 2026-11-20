// slices.rs: borrowed views into an array and into a String.
pub fn total(pages: &[u32]) -> u32 {
    // any contiguous run of u32: an array, a Vec, or a part of one
    pages.iter().sum()
}

#[allow(dead_code)]
fn main() {
    let pages = [65, 133, 412, 98, 251];
    let middle = &pages[1..4]; // elements 1, 2 and 3: a pointer and a length
    println!("{:?} {} {}", middle, total(middle), total(&pages));
    let v = vec![10, 20, 30];
    println!("{}", total(&v)); // a &Vec<u32> becomes a &[u32]

    let street = String::from("Café Lane"); // é takes two bytes in UTF-8
    let first: &str = &street[0..5]; // bytes 0 to 4: a string slice
    println!("{first:?}, {} bytes, {} chars", street.len(), street.chars().count());
    let literal: &str = "Mill Row"; // a literal is a &str into the program's data
    println!("{}", &literal[5..]);
}
