// units_asm.rs: the same computation with and without the unit types, compiled to machine code.
#[allow(dead_code)]
mod units;
use units::{Metres, MetresPerSecond, Seconds};

#[no_mangle]
pub fn trip_speed_typed(legs: &[(Metres, Seconds)]) -> MetresPerSecond {
    let (mut d, mut t) = (Metres(0.0), Seconds(0.0));
    for &(dist, time) in legs {
        d = d + dist;
        t = t + time;
    }
    d / t
}

#[no_mangle]
pub fn trip_speed_raw(legs: &[(f64, f64)]) -> f64 {
    let (mut d, mut t) = (0.0, 0.0);
    for &(dist, time) in legs {
        d += dist;
        t += time;
    }
    d / t
}
