// monthly.rs: the weekend problem's tree of monthly aggregates, keyed by (station, month).
use crate::weather::{Reading, Station};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Agg {
    pub n: u32,
    pub sum: f64,
    pub min: f64,
    pub max: f64,
}

impl Agg {
    pub fn mean(&self) -> f64 {
        self.sum / self.n as f64
    }
}

pub fn monthly(readings: &[Reading]) -> BTreeMap<(Station, u32), Agg> {
    let mut tree: BTreeMap<(Station, u32), Agg> = BTreeMap::new(); // balanced, in key order
    for r in readings {
        let month: u32 = r.date[5..7].parse().expect("dates are YYYY-MM-DD");
        tree.entry((r.station, month))
            .and_modify(|a| {
                a.n += 1;
                a.sum += r.temp_c;
                a.min = a.min.min(r.temp_c);
                a.max = a.max.max(r.temp_c);
            })
            .or_insert(Agg { n: 1, sum: r.temp_c, min: r.temp_c, max: r.temp_c });
    }
    tree
}
