// capture: exit
// nonexhaustive.rs: a match that forgot a variant.
enum Shape {
    Circle { r: f64 },
    Rect { w: f64, h: f64 },
    Triangle(f64, f64, f64),
}

fn corners(s: &Shape) -> u32 {
    match s {
        Shape::Rect { .. } => 4,
        Shape::Triangle(..) => 3,
    }
}

fn main() {
    println!("{}", corners(&Shape::Circle { r: 1.0 }));
}
