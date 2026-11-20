// display.rs: one trait, Display, and {} prints a type that println! has never seen.
use std::fmt;

struct Book {
    title: String,
    pages: u32,
}

impl fmt::Display for Book {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} ({} pages)", self.title, self.pages)
    }
}

fn main() {
    let b = Book { title: "The Paper Forest".to_string(), pages: 133 };
    println!("{b}");                          // println! calls Display::fmt
    let line = format!("[{b:>30}]");       // so does format!, with its width ignored by write!
    let owned: String = b.to_string();        // and to_string, given to every Display type
    println!("{line}\n{} characters", owned.len());
}
