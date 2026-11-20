// exo_folds.rs: predict the four values.
fn main() {
    let xs = [3, 1, 4, 1, 5];
    let a = xs.iter().fold(0, |acc, x| acc * 10 + x);
    let b = xs.iter().rev().fold(0, |acc, x| acc * 10 + x);
    let c = xs.iter().fold(Vec::new(), |mut acc, &x| { acc.insert(0, x); acc });
    let d = xs.iter().fold((i32::MAX, i32::MIN), |(lo, hi), &x| (lo.min(x), hi.max(x)));
    println!("{a} {b} {c:?} {d:?}");
}
