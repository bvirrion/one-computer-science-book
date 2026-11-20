// pmap.rs: a persistent map by path copying; every version stays readable (exercise 11).
use std::rc::Rc;

#[derive(Debug)]
struct Node<V> {
    key: u32,
    value: V,
    left: Option<Rc<Node<V>>>,
    right: Option<Rc<Node<V>>>,
}

#[derive(Debug)]
pub struct PMap<V> {
    root: Option<Rc<Node<V>>>,
}

impl<V> Clone for PMap<V> {
    fn clone(&self) -> Self {
        PMap { root: self.root.clone() } // shares everything: one count increment
    }
}

fn insert<V: Clone>(t: &Option<Rc<Node<V>>>, key: u32, value: V) -> Rc<Node<V>> {
    match t {
        None => Rc::new(Node { key, value, left: None, right: None }),
        Some(n) => {
            let (left, right) = (n.left.clone(), n.right.clone());
            let mut copy = Node { key: n.key, value: n.value.clone(), left, right };
            if key < n.key {
                copy.left = Some(insert(&n.left, key, value));
            } else if key > n.key {
                copy.right = Some(insert(&n.right, key, value));
            } else {
                copy.value = value; // the same key: a new value, in the copy only
            }
            Rc::new(copy)
        }
    }
}

impl<V: Clone> PMap<V> {
    pub fn new() -> Self {
        PMap { root: None }
    }

    pub fn insert(&self, key: u32, value: V) -> Self {
        PMap { root: Some(insert(&self.root, key, value)) }
    }

    pub fn get(&self, key: u32) -> Option<&V> {
        let mut t = &self.root;
        while let Some(n) = t {
            if key == n.key {
                return Some(&n.value);
            }
            t = if key < n.key { &n.left } else { &n.right };
        }
        None
    }
}

impl<V: Clone> Default for PMap<V> {
    fn default() -> Self {
        Self::new()
    }
}
