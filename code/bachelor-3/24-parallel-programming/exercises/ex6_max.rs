// ex6_max.rs -- the largest element of a slice, on p scoped threads: each thread finds
// the maximum of its chunk, the caller takes the maximum of the p results.
use std::thread;

pub fn par_max(a: &[i64], p: usize) -> Option<i64> {
    if a.is_empty() || p == 0 {
        return None;
    }
    let chunk = a.len().div_ceil(p);
    thread::scope(|s| {
        let hs: Vec<_> = a
            .chunks(chunk)
            .map(|c| s.spawn(move || *c.iter().max().unwrap()))
            .collect();
        hs.into_iter().map(|h| h.join().unwrap()).max()
    })
}
