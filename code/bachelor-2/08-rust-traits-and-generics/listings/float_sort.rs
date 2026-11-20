// capture: exit
// float_sort.rs: f64 is PartialOrd but not Ord, because of NaN.
use std::cmp::Ordering;

fn main() {
    std::panic::set_hook(Box::new(|p| {
        eprintln!("panicked at {}:\n{}", p.location().unwrap(), p.payload_as_str().unwrap_or("?"))
    }));
    let nan = f64::NAN;
    println!("{:?} {:?} {}", 1.0_f64.partial_cmp(&nan), nan.partial_cmp(&nan), nan == nan);
    let temps = vec![4.3, -0.1, nan, 12.5, 3.9, -2.0];
    // temps.sort();  would not compile: the trait bound `f64: Ord` is not satisfied
    let mut t = temps.clone();
    t.sort_by(f64::total_cmp); // a total order on every f64: NaN after +infinity
    println!("{t:?}");
    let mut t = temps.clone();
    t.sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal)); // "NaN equals everything"
    println!("{t:?}");
    let mut t = temps.clone();
    t.sort_by(|a, b| a.partial_cmp(b).unwrap()); // the usual shortcut
    println!("{t:?}");
}
