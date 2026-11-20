// dispatch_cost.rs: the same areas summed through a generic, an enum and trait objects.
use std::hint::black_box;
use std::time::Instant;

trait Shape {
    fn area(&self) -> f64;
}
struct Rect { w: f64, h: f64 }
struct Square { s: f64 }
impl Shape for Rect { fn area(&self) -> f64 { self.w * self.h } }
impl Shape for Square { fn area(&self) -> f64 { self.s * self.s } }

enum Any { R(Rect), S(Square) }

fn sum_generic<T: Shape>(xs: &[T]) -> f64 { xs.iter().map(|x| x.area()).sum() } // per T
fn sum_enum(xs: &[Any]) -> f64 {
    xs.iter().map(|x| match x { Any::R(r) => r.area(), Any::S(s) => s.area() }).sum()
}
fn sum_dyn(xs: &[Box<dyn Shape>]) -> f64 { xs.iter().map(|x| x.area()).sum() } // via the table

fn time(label: &str, n: usize, f: impl Fn() -> f64) {
    let start = Instant::now();
    let mut total = 0.0;
    for _ in 0..20 {
        total += black_box(f());
    }
    let ns = start.elapsed().as_nanos() as f64 / (20 * n) as f64;
    println!("{label:<22}{ns:>6.2} ns per shape   (check {total:.0})");
}

fn main() {
    let n = 1_000_000;
    let rect = |i: usize| Rect { w: (i % 7) as f64, h: 2.0 };
    let mixed: Vec<Any> =
        (0..n).map(|i| if i % 2 == 0 { Any::R(rect(i)) } else { Any::S(Square { s: 1.0 }) }).collect();
    let boxed: Vec<Box<dyn Shape>> = (0..n).map(|i| -> Box<dyn Shape> {
        if i % 2 == 0 { Box::new(rect(i)) } else { Box::new(Square { s: 1.0 }) }
    }).collect();
    let rects: Vec<Rect> = (0..n).map(rect).collect();
    time("generic, rects only", n, || sum_generic(black_box(&rects)));
    time("enum, mixed", n, || sum_enum(black_box(&mixed)));
    time("dyn, mixed", n, || sum_dyn(black_box(&boxed)));
}
