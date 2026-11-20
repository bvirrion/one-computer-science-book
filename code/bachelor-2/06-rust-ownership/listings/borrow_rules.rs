// borrow_rules.rs: shared borrows to read, an exclusive borrow to change.
fn letters(s: &str) -> usize {
    // a shared borrow: may read, may not change
    s.chars().filter(|c| c.is_alphabetic()).count()
}

fn add_suffix(s: &mut String, suffix: &str) {
    // an exclusive borrow: the only access while it lasts
    s.push(' ');
    s.push_str(suffix);
}

fn main() {
    let mut street = String::from("Mill");
    let r1 = &street;
    let r2 = &street; // any number of shared borrows at once
    println!("{} {} letters", r1, letters(r2));
    add_suffix(&mut street, "Lane"); // r1 and r2 are no longer used: allowed
    println!("{street}: {} letters", letters(&street));
    let m = &mut street;
    m.make_ascii_uppercase();
    println!("{street}"); // m's last use was the line before
}
