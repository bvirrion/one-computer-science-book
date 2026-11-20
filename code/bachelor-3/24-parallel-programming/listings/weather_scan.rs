// weather_scan.rs -- running totals of 2^24 days of rain (the town's two years, repeated),
// sequentially and with a blocked scan on p = 1..8 scoped threads, best of five runs.
use std::fs;
use std::thread;
use std::time::Instant;

pub fn scan_seq(a: &[i64], out: &mut [i64]) {
    let mut run = 0;
    for (o, v) in out.iter_mut().zip(a) {
        run += v;
        *o = run;
    }
}

/// Pass 1 sums each block, the p block sums are scanned in turn, and pass 2
/// scans each block again starting from the sum of the blocks before it.
pub fn scan_par(a: &[i64], out: &mut [i64], p: usize) {
    let block = a.len().div_ceil(p).max(1);
    let sums: Vec<i64> = thread::scope(|s| {
        let hs: Vec<_> = a
            .chunks(block)
            .map(|c| s.spawn(move || c.iter().sum()))
            .collect();
        hs.into_iter().map(|h| h.join().unwrap()).collect()
    });
    let mut offset = vec![0; sums.len()];
    for i in 1..sums.len() {
        offset[i] = offset[i - 1] + sums[i - 1];
    }
    thread::scope(|s| {
        for ((c, o), off) in a.chunks(block).zip(out.chunks_mut(block)).zip(offset) {
            s.spawn(move || {
                let mut run = off;
                for (x, v) in o.iter_mut().zip(c) {
                    run += v;
                    *x = run;
                }
            });
        }
    });
}

fn best_ms<F: FnMut()>(mut f: F) -> f64 {
    (0..5)
        .map(|_| {
            let t = Instant::now();
            f();
            t.elapsed().as_secs_f64() * 1e3
        })
        .fold(f64::INFINITY, f64::min)
}

fn main() {
    let csv = fs::read_to_string("../../../../data/town/weather.csv").unwrap();
    let rain: Vec<i64> = csv
        .lines()
        .skip(1)
        .map(|l| (l.split(',').nth(3).unwrap().parse::<f64>().unwrap() * 10.0).round() as i64)
        .collect();
    let n = 1 << 24;
    let a: Vec<i64> = (0..n).map(|i| rain[i % rain.len()]).collect();
    let (mut want, mut got) = (vec![0; n], vec![0; n]);
    let seq = best_ms(|| scan_seq(&a, &mut want));
    println!("sequential scan: {seq:.1} ms");
    println!(" p  blocked scan ms  speed-up");
    for p in 1..=8 {
        let t = best_ms(|| scan_par(&a, &mut got, p));
        assert!(got == want, "the blocked scan differs");
        println!("{p:>2} {t:>16.1} {:>9.2}", seq / t);
    }
}
