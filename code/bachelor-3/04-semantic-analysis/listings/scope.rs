// scope.rs -- a symbol table for block-structured scopes: a stack of hash
// maps, innermost last. Frozen for the book.
#![allow(dead_code)]
use std::collections::HashMap;

pub struct Scopes<T> {
    frames: Vec<HashMap<String, T>>,
    pub probes: u64, // hash-map lookups made, for the chapter's counts
}

impl<T: Clone> Scopes<T> {
    pub fn new() -> Self {
        Scopes { frames: vec![HashMap::new()], probes: 0 }
    }
    pub fn push(&mut self) {
        self.frames.push(HashMap::new());
    }
    pub fn pop(&mut self) {
        self.frames.pop();
    }
    pub fn depth(&self) -> usize {
        self.frames.len()
    }
    /// Declare in the innermost scope; a name already declared there is
    /// refused and its first declaration returned.
    pub fn declare(&mut self, name: &str, v: T) -> Result<(), T> {
        let top = self.frames.last_mut().unwrap();
        if let Some(old) = top.get(name) {
            return Err(old.clone());
        }
        top.insert(name.to_string(), v);
        Ok(())
    }
    /// The innermost declaration of `name`: search from the top of the stack.
    pub fn lookup(&mut self, name: &str) -> Option<T> {
        for frame in self.frames.iter().rev() {
            self.probes += 1;
            if let Some(v) = frame.get(name) {
                return Some(v.clone());
            }
        }
        None
    }
    /// The names of each scope, outermost first, sorted (for traces).
    pub fn names(&self) -> Vec<Vec<String>> {
        self.frames.iter().map(|f| {
            let mut v: Vec<String> = f.keys().cloned().collect();
            v.sort();
            v
        }).collect()
    }
}
