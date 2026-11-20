// largest.rs: the largest element, generic over the element type (exercise 7).
pub fn largest<T: PartialOrd + Copy>(xs: &[T]) -> Option<T> {
    let mut it = xs.iter().copied();
    let mut best = it.next()?; // None for an empty slice
    for x in it {
        if x > best {
            best = x;
        }
    }
    Some(best)
}

/// Without Copy: return a reference into the slice instead of a copy.
pub fn largest_ref<T: PartialOrd>(xs: &[T]) -> Option<&T> {
    let mut best = xs.first()?;
    for x in xs {
        if x > best {
            best = x;
        }
    }
    Some(best)
}
