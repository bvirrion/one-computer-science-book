// matrix.rs: square matrices generic over a numeric trait written here (exercise 10).
use std::ops::{Add, Mul};

pub trait Numeric: Copy + Add<Output = Self> + Mul<Output = Self> {
    fn zero() -> Self;
    fn one() -> Self;
}
impl Numeric for i64 {
    fn zero() -> Self { 0 }
    fn one() -> Self { 1 }
}
impl Numeric for f64 {
    fn zero() -> Self { 0.0 }
    fn one() -> Self { 1.0 }
}
/// bool has no Add, and the orphan rule forbids writing one here (both trait and type are foreign):
/// a newtype, with "or" as addition and "and" as multiplication.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Reach(pub bool);
impl Add for Reach {
    type Output = Reach;
    fn add(self, o: Reach) -> Reach { Reach(self.0 || o.0) }
}
impl Mul for Reach {
    type Output = Reach;
    fn mul(self, o: Reach) -> Reach { Reach(self.0 && o.0) }
}
impl Numeric for Reach {
    fn zero() -> Self { Reach(false) }
    fn one() -> Self { Reach(true) }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Matrix<T> {
    pub n: usize,
    pub a: Vec<T>, // row-major, n * n
}

impl<T: Numeric> Matrix<T> {
    pub fn identity(n: usize) -> Self {
        let mut a = vec![T::zero(); n * n];
        for i in 0..n {
            a[i * n + i] = T::one();
        }
        Matrix { n, a }
    }

    pub fn mul(&self, o: &Matrix<T>) -> Matrix<T> {
        let n = self.n;
        let mut a = vec![T::zero(); n * n];
        for i in 0..n {
            for k in 0..n {
                let x = self.a[i * n + k];
                for j in 0..n {
                    a[i * n + j] = a[i * n + j] + x * o.a[k * n + j];
                }
            }
        }
        Matrix { n, a }
    }

    pub fn pow(&self, mut e: u32) -> Matrix<T> {
        let (mut base, mut acc) = (self.clone(), Matrix::identity(self.n));
        while e > 0 {
            if e & 1 == 1 {
                acc = acc.mul(&base);
            }
            base = base.mul(&base);
            e >>= 1;
        }
        acc
    }
}
