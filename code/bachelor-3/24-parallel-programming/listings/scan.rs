// scan.rs -- prefix sums two ways, with their additions (work) and parallel steps (span)
// counted: Hillis and Steele's scan, and Blelloch's work-efficient scan, traced on the
// rain of the town's first eight days (tenths of a millimetre, Riverside).
use std::fs;

/// Inclusive scan: in round d every element adds the one 2^d places to its left.
pub fn hillis_steele(a: &[i64]) -> (Vec<i64>, u64, u32) {
    let (mut x, mut work, mut span, mut d) = (a.to_vec(), 0, 0, 1);
    while d < x.len() {
        let prev = x.clone(); // all additions of a round read the old values
        for j in d..x.len() {
            x[j] = prev[j] + prev[j - d];
            work += 1;
        }
        span += 1;
        d *= 2;
    }
    (x, work, span)
}

/// Exclusive scan in place (n a power of two): an up-sweep builds a tree of partial
/// sums, a down-sweep pushes the sums of the left subtrees down to the right.
pub fn blelloch(x: &mut [i64], trace: bool) -> (u64, u32) {
    let (n, mut work, mut span) = (x.len(), 0, 0);
    let mut d = 1;
    while d < n {
        for i in (2 * d - 1..n).step_by(2 * d) {
            x[i] += x[i - d];
            work += 1;
        }
        span += 1;
        if trace {
            println!("up   {d}: {x:?}");
        }
        d *= 2;
    }
    x[n - 1] = 0;
    while d > 1 {
        d /= 2;
        for i in (2 * d - 1..n).step_by(2 * d) {
            let left = x[i - d];
            x[i - d] = x[i];
            x[i] += left;
            work += 1;
        }
        span += 1;
        if trace {
            println!("down {d}: {x:?}");
        }
    }
    (work, span)
}

fn main() {
    let csv = fs::read_to_string("../../../../data/town/weather.csv").unwrap();
    let rain: Vec<i64> = csv
        .lines()
        .filter(|l| l.contains(",Riverside,"))
        .map(|l| (l.split(',').nth(3).unwrap().parse::<f64>().unwrap() * 10.0).round() as i64)
        .collect();
    let mut x = rain[..8].to_vec();
    println!("rain:   {x:?}");
    blelloch(&mut x, true);
    println!("     n   Hillis-Steele work span   Blelloch work span");
    for k in [4, 8, 12, 16, 20] {
        let n = 1usize << k;
        let a: Vec<i64> = (0..n).map(|i| rain[i % rain.len()]).collect();
        let (inc, hw, hs) = hillis_steele(&a);
        let mut ex = a.clone();
        let (bw, bs) = blelloch(&mut ex, false);
        let mut run = 0;
        for i in 0..n {
            assert!(
                ex[i] == run && inc[i] == run + a[i],
                "a scan is wrong at {i}"
            );
            run += a[i];
        }
        println!("{n:>7} {hw:>19} {hs:>4} {bw:>18} {bs:>4}");
    }
}
