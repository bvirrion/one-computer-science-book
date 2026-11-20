// frame.rs -- the stack frame of a function compiled naively: one word per
// temporary, then the saved return address, the size rounded up to 16.
#![allow(dead_code)]

#[derive(Clone, Copy)]
pub struct Frame {
    pub size: i32,   // bytes, a multiple of 16
    pub ra: i32,     // offset of the saved ra from sp
}

impl Frame {
    pub fn new(temps: u32) -> Frame {
        let used = 4 * temps as i32 + 4; // the temporaries, then ra
        let size = (used + 15) / 16 * 16;
        Frame { size, ra: size - 4 }
    }
    /// Offset from sp of temporary t.
    pub fn slot(&self, t: u32) -> i32 {
        4 * t as i32
    }
}
