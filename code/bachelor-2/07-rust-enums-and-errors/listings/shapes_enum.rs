// shapes_enum.rs: a sum type of three shapes, and one match that handles every one.
use std::f64::consts::PI;

#[derive(Debug)]
enum Shape {
    Circle { r: f64 },        // a variant with named fields
    Rect { w: f64, h: f64 },
    Triangle(f64, f64, f64), // a variant with unnamed fields: the three sides
}

fn area(s: &Shape) -> f64 {
    match s {
        Shape::Circle { r } => PI * r * r,
        Shape::Rect { w, h } => w * h,
        Shape::Triangle(a, b, c) => {
            let p = (a + b + c) / 2.0; // Heron's formula
            (p * (p - a) * (p - b) * (p - c)).sqrt()
        }
    }
}

fn main() {
    let plots = [
        Shape::Rect { w: 4.0, h: 5.0 },
        Shape::Circle { r: 1.5 },
        Shape::Triangle(3.0, 4.0, 5.0),
    ];
    for s in &plots {
        println!("{s:?}: area {:.2}", area(s));
    }
}
