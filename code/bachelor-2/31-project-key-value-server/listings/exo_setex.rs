// exo_setex.rs (exercise 7): SETEX k seconds v, with a clock the program controls.
use std::collections::HashMap;

struct Store {
    map: HashMap<String, (String, Option<u64>)>, // value, and the instant it expires
}

impl Store {
    fn setex(&mut self, k: &str, seconds: u64, v: &str, now: u64) {
        self.map.insert(k.to_string(), (v.to_string(), Some(now + seconds)));
    }
    fn set(&mut self, k: &str, v: &str) {
        self.map.insert(k.to_string(), (v.to_string(), None));
    }
    /// An expired key is removed when it is read: lazy expiry.
    fn get(&mut self, k: &str, now: u64) -> Option<String> {
        match self.map.get(k) {
            Some((_, Some(t))) if *t <= now => {
                self.map.remove(k);
                None
            }
            Some((v, _)) => Some(v.clone()),
            None => None,
        }
    }
    /// The keys nobody reads stay until a sweep removes them.
    fn sweep(&mut self, now: u64) -> usize {
        let before = self.map.len();
        self.map.retain(|_, (_, t)| t.is_none_or(|t| t > now));
        before - self.map.len()
    }
}

fn main() {
    let mut s = Store { map: HashMap::new() };
    s.setex("session:ada", 30, "token-1", 0);
    s.setex("reservation:7", 3600, "member-55", 0);
    s.setex("old:1", 10, "x", 0);
    s.set("loan:3", "out");
    for now in [0, 29, 30] {
        println!("t = {now:>4} s: GET session:ada -> {:?}", s.get("session:ada", now));
    }
    println!("t = 3600 s: keys before the sweep {}", s.map.len());
    println!("            the sweep removes {}, {} left", s.sweep(3600), s.map.len());
}
