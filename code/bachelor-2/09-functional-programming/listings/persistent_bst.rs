// persistent_bst.rs: a search tree whose insert makes a new version and keeps the old one.
use std::collections::HashSet;
use std::rc::Rc;

#[derive(Debug)]
pub struct Node {
    pub key: i32,
    pub left: Tree,
    pub right: Tree,
}
pub type Tree = Option<Rc<Node>>;

pub fn insert(t: &Tree, k: i32) -> Tree {
    match t {
        None => Some(Rc::new(Node { key: k, left: None, right: None })),
        Some(n) if k < n.key => {
            let left = insert(&n.left, k); // a new left subtree; the right one is shared
            Some(Rc::new(Node { key: n.key, left, right: n.right.clone() }))
        }
        Some(n) if k > n.key => {
            let right = insert(&n.right, k);
            Some(Rc::new(Node { key: n.key, left: n.left.clone(), right }))
        }
        Some(_) => t.clone(), // already there: shared (the path above is still copied)
    }
}

/// Adds the address of every node of t to seen; returns how many were new.
pub fn mark(t: &Tree, seen: &mut HashSet<*const Node>) -> usize {
    match t {
        None => 0,
        Some(n) => {
            let new = seen.insert(Rc::as_ptr(n)) as usize;
            new + mark(&n.left, seen) + mark(&n.right, seen)
        }
    }
}

pub fn keys(t: &Tree, out: &mut Vec<i32>) {
    if let Some(n) = t {
        keys(&n.left, out);
        out.push(n.key);
        keys(&n.right, out);
    }
}

#[allow(dead_code)]
fn main() {
    let mut v1 = None;
    for k in [189, 65, 251, 133, 412, 98, 320] {
        v1 = insert(&v1, k);
    }
    let v2 = insert(&v1, 140); // 189 -> 65 -> 133 -> (right) 140: three nodes copied, one new
    let mut seen = HashSet::new();
    let (n1, n2) = (mark(&v1, &mut seen), mark(&v2, &mut seen));
    let (mut k1, mut k2) = (Vec::new(), Vec::new());
    keys(&v1, &mut k1);
    keys(&v2, &mut k2);
    println!("v1 {k1:?}\nv2 {k2:?}");
    println!("nodes: v1 {n1}, new in v2 {n2}, shared {}", k2.len() - n2);
}
