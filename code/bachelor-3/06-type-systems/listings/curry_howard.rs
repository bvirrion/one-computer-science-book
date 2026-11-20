// curry_howard.rs -- three proofs in propositional logic, written as
// generic Rust functions: a type is a proposition, a value is a proof.

/// (A and B) implies (B and A)
fn swap<A, B>(p: (A, B)) -> (B, A) {
    (p.1, p.0)
}

/// From A implies B, and A, conclude B (modus ponens).
fn modus_ponens<A, B>(f: impl Fn(A) -> B, a: A) -> B {
    f(a)
}

/// (A implies B) and (B implies C) give (A implies C).
fn chain<A, B, C>(f: impl Fn(A) -> B, g: impl Fn(B) -> C) -> impl Fn(A) -> C {
    move |a| g(f(a))
}

fn main() {
    let proof = swap((1, "one"));
    let len_is_even = chain(|s: &str| s.len(), |n: usize| n % 2 == 0);
    println!("{proof:?} {} {}", modus_ponens(&len_is_even, "four"), len_is_even("odd"));
}
