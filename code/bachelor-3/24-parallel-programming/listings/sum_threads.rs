// sum_threads.rs -- one job split over p scoped threads, timed for p = 1..8:
// a memory-bound sum of 2^25 numbers, and a compute-bound loop over as many.
use std::thread;
use std::time::Instant;

fn mix(mut x: u64) -> u64 {
    for _ in 0..40 {
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
    }
    x
}

fn sum_mem(data: &[u32], p: usize) -> u64 {
    let chunk = data.len().div_ceil(p);
    thread::scope(|s| {
        let parts: Vec<_> = data
            .chunks(chunk)
            .map(|c| s.spawn(move || c.iter().map(|&v| v as u64).sum::<u64>()))
            .collect();
        parts.into_iter().map(|h| h.join().unwrap()).sum()
    })
}

fn sum_cpu(n: u64, p: u64) -> u64 {
    thread::scope(|s| {
        let parts: Vec<_> = (0..p)
            .map(|t| {
                s.spawn(move || {
                    (t * n / p..(t + 1) * n / p)
                        .map(mix)
                        .fold(0, u64::wrapping_add)
                })
            })
            .collect();
        parts
            .into_iter()
            .map(|h| h.join().unwrap())
            .fold(0, u64::wrapping_add)
    })
}

fn best_ms<F: FnMut() -> u64>(mut f: F) -> (f64, u64) {
    let mut best = f64::INFINITY;
    let mut out = 0;
    for _ in 0..5 {
        let t = Instant::now();
        out = f();
        best = best.min(t.elapsed().as_secs_f64() * 1e3);
    }
    (best, out)
}

fn main() {
    let n = 1usize << 25;
    let data: Vec<u32> = (0..n as u32)
        .map(|i| i.wrapping_mul(2654435761) >> 20)
        .collect();
    let mut base = (0.0, 0.0, 0, 0);
    println!(" p   memory-bound ms  speed-up   compute-bound ms  speed-up");
    for p in 1..=8 {
        let (m, s) = best_ms(|| sum_mem(&data, p));
        let (c, x) = best_ms(|| sum_cpu(n as u64, p as u64));
        if p == 1 {
            base = (m, c, s, x);
        }
        assert!(
            s == base.2 && x == base.3,
            "a parallel sum differs from the serial one"
        );
        println!(
            "{p:>2} {m:>16.1} {:>9.2} {c:>18.1} {:>9.2}",
            base.0 / m,
            base.1 / c
        );
    }
}
