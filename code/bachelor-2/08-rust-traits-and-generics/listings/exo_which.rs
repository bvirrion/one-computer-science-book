// exo_which.rs: which implementation runs? Predict the five lines.
trait Greet {
    fn name(&self) -> String;
    fn hello(&self) -> String {
        format!("hello, {}", self.name())
    }
}

struct Ada;
struct Bob;

impl Greet for Ada {
    fn name(&self) -> String { "Ada".into() }
}
impl Greet for Bob {
    fn name(&self) -> String { "Bob".into() }
    fn hello(&self) -> String { format!("hi, {}", self.name()) }
}
impl Bob {
    fn name(&self) -> String { "Robert".into() } // an inherent method with the same name
}

fn twice<T: Greet>(x: &T) -> String { format!("{} / {}", x.hello(), x.name()) }

fn main() {
    let (a, b) = (Ada, Bob);
    println!("{}", a.hello());
    println!("{}", b.hello());
    println!("{}", b.name());
    println!("{}", twice(&b));
    let all: [&dyn Greet; 2] = [&a, &b];
    println!("{}", all.iter().map(|g| g.name()).collect::<Vec<_>>().join(", "));
}
