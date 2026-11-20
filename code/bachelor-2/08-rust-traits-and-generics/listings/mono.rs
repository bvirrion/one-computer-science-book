// mono.rs: one generic function, used at two types.
pub fn largest<T: PartialOrd + Copy>(xs: &[T]) -> T {
    let mut best = xs[0];
    for &x in xs {
        if x > best {
            best = x;
        }
    }
    best
}

pub fn largest_pages(pages: &[u32]) -> u32 {
    largest(pages) // instantiates largest::<u32>
}

pub fn warmest(temps: &[f64]) -> f64 {
    largest(temps) // instantiates largest::<f64>
}
