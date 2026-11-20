// checked.rs: division and mean that report impossible cases as None (exercise 3).
pub fn checked_div(a: i32, b: i32) -> Option<i32> {
    match (a, b) {
        (_, 0) => None,            // division by zero
        (i32::MIN, -1) => None,    // the quotient 2^31 does not fit in an i32
        _ => Some(a / b),
    }
}

pub fn mean(xs: &[f64]) -> Option<f64> {
    if xs.is_empty() {
        None
    } else {
        Some(xs.iter().sum::<f64>() / xs.len() as f64)
    }
}
