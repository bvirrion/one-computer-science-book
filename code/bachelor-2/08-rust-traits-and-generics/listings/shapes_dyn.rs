// shapes_dyn.rs: different types in one vector, through trait objects.
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> &'static str;
}

struct Circle { r: f64 }
struct Rect { w: f64, h: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.r * self.r }
    fn name(&self) -> &'static str { "circle" }
}

impl Shape for Rect {
    fn area(&self) -> f64 { self.w * self.h }
    fn name(&self) -> &'static str { "rect" }
}

fn total_area(shapes: &[Box<dyn Shape>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum() // each call goes through the object's table
}

fn main() {
    let plots: Vec<Box<dyn Shape>> = vec![
        Box::new(Rect { w: 4.0, h: 5.0 }),
        Box::new(Circle { r: 1.5 }),
        Box::new(Rect { w: 2.0, h: 2.5 }),
    ];
    for s in &plots {
        println!("{:<7}{:>6.2}", s.name(), s.area());
    }
    println!("total  {:>6.2}", total_area(&plots));
}
