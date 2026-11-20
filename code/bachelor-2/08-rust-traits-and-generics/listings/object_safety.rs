// capture: exit
// object_safety.rs: a trait whose method returns Self cannot be used as dyn.
trait Duplicate {
    fn duplicate(&self) -> Self; // the caller must know the size of Self
}

struct Card { number: u32 }

impl Duplicate for Card {
    fn duplicate(&self) -> Self { Card { number: self.number } }
}

fn main() {
    let cards: Vec<Box<dyn Duplicate>> = vec![Box::new(Card { number: 7 })];
    println!("{}", cards.len());
}
