// ex5_flat_fixed.rs -- exercise 5: one hash map from each name to the stack
// of its visible declarations; a block's exit pops what it pushed.
#![allow(dead_code)]
use std::collections::HashMap;

pub struct Flat {
    map: HashMap<String, Vec<u32>>,
    blocks: Vec<Vec<String>>,
    pub probes: u64,
}

impl Flat {
    pub fn new() -> Self {
        Flat { map: HashMap::new(), blocks: vec![], probes: 0 }
    }
    pub fn enter(&mut self) {
        self.blocks.push(Vec::new());
    }
    pub fn declare(&mut self, name: &str, line: u32) {
        self.map.entry(name.to_string()).or_default().push(line);
        self.blocks.last_mut().unwrap().push(name.to_string());
    }
    pub fn exit(&mut self) {
        for name in self.blocks.pop().unwrap() {
            let stack = self.map.get_mut(&name).unwrap();
            stack.pop();
            if stack.is_empty() {
                self.map.remove(&name);
            }
        }
    }
    pub fn lookup(&mut self, name: &str) -> Option<u32> {
        self.probes += 1;
        self.map.get(name).and_then(|s| s.last().copied())
    }
}
