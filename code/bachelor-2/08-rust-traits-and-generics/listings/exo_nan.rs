// exo_nan.rs: the median of a station's temperatures; one field held the text "NaN".
use std::cmp::Ordering;

fn median(xs: &mut [f64]) -> f64 {
    xs.sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
    xs[xs.len() / 2]
}

fn main() {
    let fields = ["4.3", "3.9", "NaN", "5.1", "-0.4", "2.8", "6.0"];
    let mut temps: Vec<f64> = fields.iter().map(|f| f.parse().unwrap()).collect(); // takes NaN
    println!("median {}", median(&mut temps));
    println!("{temps:?}");
}
