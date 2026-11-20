// sizes.rs: how many bytes each type takes: tag, payload, and the niche of references.
use std::mem::size_of;

#[allow(dead_code)]
enum Shape {
    Circle { r: f64 },
    Rect { w: f64, h: f64 },
    Triangle(f64, f64, f64),
}

fn row(name: &str, bytes: usize) {
    println!("{name:<22}{bytes:>3}");
}

fn main() {
    row("u32", size_of::<u32>());
    row("Option<u32>", size_of::<Option<u32>>()); // a tag beside the u32
    row("&u32", size_of::<&u32>());
    row("Option<&u32>", size_of::<Option<&u32>>()); // None is the null address
    row("Box<u32>", size_of::<Box<u32>>());
    row("Option<Box<u32>>", size_of::<Option<Box<u32>>>());
    row("Shape", size_of::<Shape>()); // three f64s and a tag
    row("Option<bool>", size_of::<Option<bool>>()); // bool uses 2 of 256 values
    row("Result<u32, String>", size_of::<Result<u32, String>>());
}
