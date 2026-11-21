// fat_pointer.rs: a reference to a trait object is two pointers; read them.
use std::mem::size_of;

trait Shape {
    fn area(&self) -> f64;
}
struct Circle { r: f64 }
struct Rect { w: f64, h: f64 }
impl Shape for Circle { fn area(&self) -> f64 { 3.0 * self.r * self.r } }
impl Shape for Rect { fn area(&self) -> f64 { self.w * self.h } }

fn parts(s: &dyn Shape) -> (usize, usize) {
    // a &dyn Shape is (value's address, table's address): today's order, not a promise
    let [data, table]: [usize; 2] = unsafe { std::mem::transmute(s) };
    (data, table)
}

fn main() {
    println!("&Circle {}  &dyn Shape {}  Box<dyn Shape> {}  &[u32] {}  &str {}",
        size_of::<&Circle>(), size_of::<&dyn Shape>(), size_of::<Box<dyn Shape>>(),
        size_of::<&[u32]>(), size_of::<&str>());
    let (c1, c2, r) = (Circle { r: 1.0 }, Circle { r: 2.0 }, Rect { w: 1.0, h: 2.0 });
    let (d1, t1) = parts(&c1);
    let (d2, t2) = parts(&c2);
    let (d3, t3) = parts(&r);
    let shapes: [&dyn Shape; 3] = [&c1, &c2, &r];
    println!("areas {:?}", shapes.map(|s| s.area()));
    println!("data pointers differ: {}", d1 != d2 && d2 != d3);
    println!("two circles share a table: {}; the rect has its own: {}", t1 == t2, t1 != t3);
}
