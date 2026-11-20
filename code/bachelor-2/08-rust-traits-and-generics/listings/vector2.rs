// vector2.rs: operators are traits: a + b is Add::add(a, b).
use std::ops::{Add, Mul, Neg, Sub};

#[derive(Debug, Clone, Copy, PartialEq, Default)]
pub struct V2 {
    pub x: f64,
    pub y: f64,
}

impl Add for V2 {
    type Output = V2; // an associated type: the type of a + b
    fn add(self, o: V2) -> V2 { V2 { x: self.x + o.x, y: self.y + o.y } }
}

impl Sub for V2 {
    type Output = V2;
    fn sub(self, o: V2) -> V2 { V2 { x: self.x - o.x, y: self.y - o.y } }
}

impl Mul<f64> for V2 {
    type Output = V2; // V2 * f64; f64 * V2 would need impl Mul<V2> for f64
    fn mul(self, k: f64) -> V2 { V2 { x: self.x * k, y: self.y * k } }
}

impl Neg for V2 {
    type Output = V2;
    fn neg(self) -> V2 { V2 { x: -self.x, y: -self.y } }
}

#[allow(dead_code)]
fn main() {
    let library = V2 { x: 2.0, y: 1.0 };
    let station = V2 { x: 5.0, y: 5.0 };
    let walk = station - library;
    println!("{:?} {:?} {:?}", walk, library + walk * 0.5, -walk);
    println!("{:?} {}", V2::default(), library + walk == station);
}
