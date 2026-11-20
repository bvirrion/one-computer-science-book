// bounds.rs: a trait with a default method, two implementations, and generic functions over it.
use std::fmt::Display;

trait Lendable {
    fn title(&self) -> String;
    fn loan_days(&self) -> u32; // required: each type says its own

    fn describe(&self) -> String {
        // a default method: written once, in terms of the required ones
        format!("{}, lent for {} days", self.title(), self.loan_days())
    }
}

struct Book { title: String }
struct Film { title: String, minutes: u32 }

impl Lendable for Book {
    fn title(&self) -> String { self.title.clone() }
    fn loan_days(&self) -> u32 { 21 }
}

impl Lendable for Film {
    fn title(&self) -> String { format!("{} (film)", self.title) }
    fn loan_days(&self) -> u32 { 7 }
    fn describe(&self) -> String {
        // overrides the default
        format!("{}, {} min, back within {} days", self.title(), self.minutes, self.loan_days())
    }
}

fn longest_loan<T: Lendable>(items: &[T]) -> u32 {
    items.iter().map(|i| i.loan_days()).max().unwrap_or(0)
}

fn label<T>(item: &T, shelf: impl Display) -> String
where
    T: Lendable,
{
    format!("[{shelf}] {}", item.describe())
}

fn main() {
    let books = [Book { title: "The Silent Code".into() },
        Book { title: "Seven Comets".into() }];
    let film = Film { title: "Harbour Lights".into(), minutes: 94 };
    println!("{}", label(&books[0], 'B'));
    println!("{}", label(&film, 12));
    println!("{}", longest_loan(&books));
}
