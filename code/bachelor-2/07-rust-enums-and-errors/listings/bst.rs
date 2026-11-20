// bst.rs: a binary search tree as a recursive enum, each child owned through a Box.
#[derive(Debug, Default, Clone, PartialEq)]
pub enum Tree {
    #[default]
    Leaf,
    Node(Box<Tree>, i32, Box<Tree>), // left subtree, key, right subtree
}
use std::cmp::Ordering;
use Tree::*;

impl Tree {
    pub fn insert(&mut self, k: i32) {
        match self {
            Leaf => *self = Node(Box::new(Leaf), k, Box::new(Leaf)),
            Node(left, key, right) => match k.cmp(key) {
                Ordering::Less => left.insert(k),
                Ordering::Greater => right.insert(k),
                Ordering::Equal => {} // already there
            },
        }
    }

    pub fn contains(&self, k: i32) -> bool {
        match self {
            Leaf => false,
            Node(l, key, r) => k == *key || if k < *key { l.contains(k) } else { r.contains(k) },
        }
    }

    pub fn height(&self) -> usize {
        match self {
            Leaf => 0,
            Node(l, _, r) => 1 + l.height().max(r.height()),
        }
    }

    pub fn in_order(&self, out: &mut Vec<i32>) {
        if let Node(l, key, r) = self {
            l.in_order(out);
            out.push(*key);
            r.in_order(out);
        }
    }
}

#[allow(dead_code)]
fn main() {
    let mut t = Tree::default();
    for pages in [189, 65, 251, 133, 412, 98, 320] {
        t.insert(pages);
    }
    let mut keys = Vec::new();
    t.in_order(&mut keys);
    println!("{keys:?}, height {}, contains 98: {}, contains 99: {}", t.height(), t.contains(98), t.contains(99));
}
