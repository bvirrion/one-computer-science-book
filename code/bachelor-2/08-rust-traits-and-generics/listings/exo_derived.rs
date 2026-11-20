// exo_derived.rs: derived orders on a struct and an enum. Predict the two sorted lists.
#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Shelf {
    Returns,
    Fiction(char), // the first letter of the author's name
    Reference,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Loan {
    due_day: u32,
    title: &'static str,
}

fn main() {
    let mut shelves =
        vec![Shelf::Reference, Shelf::Fiction('M'), Shelf::Returns, Shelf::Fiction('B')];
    shelves.sort();
    println!("{shelves:?}");
    let mut loans = vec![
        Loan { due_day: 12, title: "Seven Comets" },
        Loan { due_day: 3, title: "The Paper Forest" },
        Loan { due_day: 12, title: "Harbour Lights" },
    ];
    loans.sort();
    println!("{:?}", loans.iter().map(|l| l.title).collect::<Vec<_>>());
}
