// scope_bug.rs -- a symbol table in one hash map, each block remembering
// the names it declared so that they can be removed at its end.
use std::collections::HashMap;

struct Flat {
    map: HashMap<String, u32>, // name -> line of its declaration
    blocks: Vec<Vec<String>>,  // names declared by each open block
}

impl Flat {
    fn enter(&mut self) {
        self.blocks.push(Vec::new());
    }
    fn declare(&mut self, name: &str, line: u32) {
        self.map.insert(name.to_string(), line);
        self.blocks.last_mut().unwrap().push(name.to_string());
    }
    fn exit(&mut self) {
        for name in self.blocks.pop().unwrap() {
            self.map.remove(&name);
        }
    }
    fn lookup(&self, name: &str) -> Option<u32> {
        self.map.get(name).copied()
    }
}

fn main() {
    let mut s = Flat { map: HashMap::new(), blocks: vec![] };
    s.enter();
    s.declare("x", 15);
    s.enter();
    s.declare("x", 17);
    println!("x in the inner block: {:?}", s.lookup("x"));
    s.exit();
    println!("x after the block:    {:?}", s.lookup("x"));
}
