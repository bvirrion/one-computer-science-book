// split.rs: two exclusive borrows of the two halves of one slice (exercise 7).
/// Adds each element of the first half to the matching element of the second half.
pub fn add_halves(v: &mut [i32]) {
    let mid = v.len() / 2;
    let (left, right) = v.split_at_mut(mid); // two &mut [i32] that cannot overlap
    for (r, l) in right.iter_mut().zip(left.iter()) {
        *r += *l;
    }
}

/// The largest element moved to the front, by swapping it with the first.
pub fn largest_first(v: &mut [i32]) {
    if let Some((first, rest)) = v.split_first_mut() {
        if let Some(big) = rest.iter_mut().max_by_key(|x| **x) {
            if *big > *first {
                std::mem::swap(first, big);
            }
        }
    }
}
