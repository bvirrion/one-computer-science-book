// capture: exit
// units_mix.rs: the mistakes the types refuse.
#[allow(dead_code)]
mod units;
use units::{Metres, Seconds};

fn main() {
    let d = Metres(400.0);
    let t = Seconds(310.0);
    let wrong = d + t;          // a length plus a time
    let raw: f64 = d;           // a length used as a bare number
    println!("{wrong:?} {raw}");
}
