// units.rs: newtypes for lengths and times; only the meaningful operations exist.
use std::fmt;
use std::ops::{Add, Div, Mul};

#[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
pub struct Metres(pub f64);
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
pub struct Seconds(pub f64);
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
pub struct MetresPerSecond(pub f64);

impl Add for Metres {
    type Output = Metres;
    fn add(self, o: Metres) -> Metres { Metres(self.0 + o.0) }
}
impl Add for Seconds {
    type Output = Seconds;
    fn add(self, o: Seconds) -> Seconds { Seconds(self.0 + o.0) }
}
impl Div<Seconds> for Metres {
    type Output = MetresPerSecond; // a length over a time is a speed
    fn div(self, t: Seconds) -> MetresPerSecond { MetresPerSecond(self.0 / t.0) }
}
impl Mul<Seconds> for MetresPerSecond {
    type Output = Metres; // a speed times a time is a length
    fn mul(self, t: Seconds) -> Metres { Metres(self.0 * t.0) }
}
impl fmt::Display for MetresPerSecond {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "{:.2} m/s", self.0) }
}

#[allow(dead_code)]
fn main() {
    let legs = [(Metres(400.0), Seconds(310.0)), (Metres(1250.0), Seconds(845.0))];
    let (mut d, mut t) = (Metres(0.0), Seconds(0.0));
    for (dist, time) in legs {
        d = d + dist;
        t = t + time;
    }
    let v = d / t;
    println!("{d:?} in {t:?}: {v}, so {:?} in an hour", v * Seconds(3600.0));
}
