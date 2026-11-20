// compose.rs: function composition, returning a closure (exercise 3).
pub fn compose<A, B, C>(f: impl Fn(B) -> C, g: impl Fn(A) -> B) -> impl Fn(A) -> C {
    move |x| f(g(x)) // first g, then f: (f o g)(x) = f(g(x))
}

/// The composition of a list of functions of one type, applied from the last to the first.
pub fn compose_all<T>(fs: Vec<Box<dyn Fn(T) -> T>>) -> impl Fn(T) -> T {
    move |x| fs.iter().rev().fold(x, |acc, f| f(acc))
}
