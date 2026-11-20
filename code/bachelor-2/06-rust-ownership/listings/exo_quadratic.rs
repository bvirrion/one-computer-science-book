// exo_quadratic.rs: the distinct street names of a list, as a port wrote it to please the borrow checker.
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering::Relaxed};

struct Counting;
static ALLOCS: AtomicUsize = AtomicUsize::new(0);
unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 { ALLOCS.fetch_add(1, Relaxed); unsafe { System.alloc(l) } }
    unsafe fn dealloc(&self, p: *mut u8, l: Layout) { unsafe { System.dealloc(p, l) } }
}
#[global_allocator]
static A: Counting = Counting;

fn distinct(names: &[String]) -> Vec<String> {
    let mut seen: Vec<String> = Vec::new();
    for n in names {
        let known = seen.clone(); // "cannot borrow `seen`": cloned to make it compile
        if !known.contains(n) {
            seen.push(n.clone());
        }
    }
    seen
}

fn main() {
    for n in [100, 200, 400] {
        let names: Vec<String> = (0..n).map(|i| format!("Street {}", i % (n / 2))).collect(); // each twice
        let before = ALLOCS.load(Relaxed);
        let d = distinct(&names);
        println!("n = {n}: {} distinct, {} allocations", d.len(), ALLOCS.load(Relaxed) - before);
    }
}
