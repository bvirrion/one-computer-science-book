// option_demo.rs: a search that may find nothing, and the ways to handle the absence.
struct Book {
    title: &'static str,
    pages: u32,
}

fn find<'a>(books: &'a [Book], title: &str) -> Option<&'a Book> {
    books.iter().find(|b| b.title == title) // Some(&book) or None: never a null pointer
}

fn pages_of_both(books: &[Book], a: &str, b: &str) -> Option<u32> {
    let x = find(books, a)?; // ? : if None, return None from pages_of_both now
    let y = find(books, b)?;
    Some(x.pages + y.pages)
}

fn main() {
    let books = [
        Book { title: "The Silent Code", pages: 65 },
        Book { title: "The Paper Forest", pages: 133 },
    ];
    match find(&books, "The Paper Forest") {
        Some(b) => println!("found, {} pages", b.pages),
        None => println!("not found"),
    }
    if let Some(b) = find(&books, "Seven Comets") {
        println!("{} pages", b.pages); // not run: the pattern does not match None
    }
    let n = find(&books, "Seven Comets").map(|b| b.pages).unwrap_or(0);
    println!("{n} {:?} {:?}", pages_of_both(&books, "The Silent Code", "The Paper Forest"),
             pages_of_both(&books, "The Silent Code", "Seven Comets"));
}
