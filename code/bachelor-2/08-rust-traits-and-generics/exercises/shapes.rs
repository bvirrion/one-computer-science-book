// shapes.rs: a collection of shapes as trait objects (exercise 9).
pub trait Shape {
    fn area(&self) -> f64;
    fn perimeter(&self) -> f64;
    fn name(&self) -> String;
}

pub struct Circle(pub f64);
pub struct Rect(pub f64, pub f64);
pub struct Triangle(pub f64, pub f64, pub f64);

impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.0 * self.0 }
    fn perimeter(&self) -> f64 { 2.0 * std::f64::consts::PI * self.0 }
    fn name(&self) -> String { format!("circle r={}", self.0) }
}
impl Shape for Rect {
    fn area(&self) -> f64 { self.0 * self.1 }
    fn perimeter(&self) -> f64 { 2.0 * (self.0 + self.1) }
    fn name(&self) -> String { format!("rect {}x{}", self.0, self.1) }
}
impl Shape for Triangle {
    fn area(&self) -> f64 {
        let p = self.perimeter() / 2.0;
        (p * (p - self.0) * (p - self.1) * (p - self.2)).sqrt()
    }
    fn perimeter(&self) -> f64 { self.0 + self.1 + self.2 }
    fn name(&self) -> String { format!("triangle {}-{}-{}", self.0, self.1, self.2) }
}

/// The names, largest area first.
pub fn by_area(shapes: &mut [Box<dyn Shape>]) -> Vec<String> {
    shapes.sort_by(|a, b| b.area().total_cmp(&a.area()));
    shapes.iter().map(|s| s.name()).collect()
}
