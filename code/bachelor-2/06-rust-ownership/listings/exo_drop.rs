// exo_drop.rs: predict the order of the lines.
struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn consume(n: Noisy) {
    println!("consume {}", n.0);
}

fn main() {
    let _a = Noisy("a");
    let b = Noisy("b");
    let _ = Noisy("c");
    let v = vec![Noisy("d"), Noisy("e")];
    consume(b);
    {
        let _f = Noisy("f");
        println!("end of block");
    }
    let _a = Noisy("a2"); // shadows _a, which still lives
    drop(v);
    println!("end of main");
}
