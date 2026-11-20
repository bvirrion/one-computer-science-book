// ex11_persistent.rs -- exercise 11: persistent scopes. A scope is an
// immutable balanced search tree (AVL); declaring copies one path and shares
// the rest, so entering a block keeps the old root and leaving it is free.
#![allow(dead_code)]
use std::rc::Rc;

type Link = Option<Rc<Node>>;

pub struct Node {
    key: String,
    val: u32,
    height: u32,
    left: Link,
    right: Link,
}

#[derive(Default)]
pub struct Counts {
    pub nodes: u64,       // nodes allocated
    pub comparisons: u64, // key comparisons in lookups
}

fn h(t: &Link) -> u32 {
    t.as_ref().map_or(0, |n| n.height)
}

fn node(key: String, val: u32, left: Link, right: Link, c: &mut Counts) -> Link {
    c.nodes += 1;
    let height = 1 + h(&left).max(h(&right));
    Some(Rc::new(Node { key, val, height, left, right }))
}

fn balance(key: String, val: u32, l: Link, r: Link, c: &mut Counts) -> Link {
    let (hl, hr) = (h(&l), h(&r));
    if hl > hr + 1 {
        let n = l.unwrap();
        if h(&n.left) >= h(&n.right) {
            let right = node(key, val, n.right.clone(), r, c);
            node(n.key.clone(), n.val, n.left.clone(), right, c)
        } else {
            let m = n.right.as_ref().unwrap();
            let left = node(n.key.clone(), n.val, n.left.clone(), m.left.clone(), c);
            let right = node(key, val, m.right.clone(), r, c);
            node(m.key.clone(), m.val, left, right, c)
        }
    } else if hr > hl + 1 {
        let n = r.unwrap();
        if h(&n.right) >= h(&n.left) {
            let left = node(key, val, l, n.left.clone(), c);
            node(n.key.clone(), n.val, left, n.right.clone(), c)
        } else {
            let m = n.left.as_ref().unwrap();
            let left = node(key, val, l, m.left.clone(), c);
            let right = node(n.key.clone(), n.val, m.right.clone(), n.right.clone(), c);
            node(m.key.clone(), m.val, left, right, c)
        }
    } else {
        node(key, val, l, r, c)
    }
}

/// A new tree with `key` bound to `val` (replacing an outer binding of the
/// same name); `t` itself is unchanged.
pub fn insert(t: &Link, key: &str, val: u32, c: &mut Counts) -> Link {
    match t {
        None => node(key.to_string(), val, None, None, c),
        Some(n) => match key.cmp(&n.key) {
            std::cmp::Ordering::Less => {
                let l = insert(&n.left, key, val, c);
                balance(n.key.clone(), n.val, l, n.right.clone(), c)
            }
            std::cmp::Ordering::Greater => {
                let r = insert(&n.right, key, val, c);
                balance(n.key.clone(), n.val, n.left.clone(), r, c)
            }
            std::cmp::Ordering::Equal => node(key.to_string(), val, n.left.clone(), n.right.clone(), c),
        },
    }
}

pub fn lookup(t: &Link, key: &str, c: &mut Counts) -> Option<u32> {
    let mut cur = t;
    while let Some(n) = cur {
        c.comparisons += 1;
        match key.cmp(&n.key) {
            std::cmp::Ordering::Less => cur = &n.left,
            std::cmp::Ordering::Greater => cur = &n.right,
            std::cmp::Ordering::Equal => return Some(n.val),
        }
    }
    None
}

pub fn height(t: &Link) -> u32 {
    h(t)
}
