// exo_clones.rs: how many heap allocations does main make? A counting allocator answers.
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering::Relaxed};

struct Counting; // forwards to the system allocator, counting the calls
static ALLOCS: AtomicUsize = AtomicUsize::new(0);
static REALLOCS: AtomicUsize = AtomicUsize::new(0);
unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 { ALLOCS.fetch_add(1, Relaxed); unsafe { System.alloc(l) } }
    unsafe fn dealloc(&self, p: *mut u8, l: Layout) { unsafe { System.dealloc(p, l) } }
    unsafe fn realloc(&self, p: *mut u8, l: Layout, n: usize) -> *mut u8 {
        REALLOCS.fetch_add(1, Relaxed);
        unsafe { System.realloc(p, l, n) }
    }
}
#[global_allocator]
static A: Counting = Counting;

fn main() {
    let before = ALLOCS.load(Relaxed);
    let a = String::from("Mill");
    let b = a.clone();
    let mut v: Vec<String> = Vec::new();
    v.push(b);
    v.push(a.clone());
    let c = v[0].clone() + " Lane";
    let d = &c;
    let e = d.to_uppercase();
    let total = ALLOCS.load(Relaxed) - before;
    println!("{total} allocations, {} reallocations ({a} {c} {e} {})",
        REALLOCS.load(Relaxed), v.len());
}
