// sheet.rs: a spreadsheet whose every edit makes a new version, sharing all it did not change.
use std::cell::Cell as Counter;
use std::collections::HashSet;
use std::rc::Rc;

pub type Formula = Rc<dyn Fn(&Sheet) -> f64>; // reads other cells of the same version

#[derive(Clone)]
pub enum Cell {
    Num(f64),
    Formula(Formula),
}

pub struct Node {
    key: u32,
    cell: Cell,
    left: Link,
    right: Link,
}
type Link = Option<Rc<Node>>;

#[derive(Clone)]
pub struct Sheet {
    root: Link,
    pub evaluations: Rc<Counter<u32>>, // formulas run so far, shared by all versions
}

fn build(cells: &[(u32, Cell)]) -> Link {
    if cells.is_empty() {
        return None;
    }
    let mid = cells.len() / 2; // the middle key at the root: a balanced tree
    let (key, cell) = cells[mid].clone();
    let (left, right) = (build(&cells[..mid]), build(&cells[mid + 1..]));
    Some(Rc::new(Node { key, cell, left, right }))
}

fn set(t: &Link, key: u32, cell: Cell) -> Link {
    let n = t.as_ref().expect("only existing cells are set");
    let (left, right, cell) = if key < n.key {
        (set(&n.left, key, cell), n.right.clone(), n.cell.clone())
    } else if key > n.key {
        (n.left.clone(), set(&n.right, key, cell), n.cell.clone())
    } else {
        (n.left.clone(), n.right.clone(), cell)
    };
    Some(Rc::new(Node { key: n.key, cell, left, right })) // one new node per level of the path
}

impl Sheet {
    pub fn new(cells: &[(u32, Cell)]) -> Sheet {
        Sheet { root: build(cells), evaluations: Rc::new(Counter::new(0)) }
    }

    pub fn set(&self, key: u32, cell: Cell) -> Sheet {
        Sheet { root: set(&self.root, key, cell), evaluations: Rc::clone(&self.evaluations) }
    }

    fn get(&self, key: u32) -> &Cell {
        let mut t = &self.root;
        while let Some(n) = t {
            if key == n.key {
                return &n.cell;
            }
            t = if key < n.key { &n.left } else { &n.right };
        }
        panic!("no cell {key}")
    }

    /// The value of a cell; a formula runs only now, when its value is asked for.
    pub fn value(&self, key: u32) -> f64 {
        match self.get(key) {
            Cell::Num(x) => *x,
            Cell::Formula(f) => {
                self.evaluations.set(self.evaluations.get() + 1);
                f(self)
            }
        }
    }
}

/// The number of distinct nodes reachable from all the versions together.
pub fn distinct_nodes(versions: &[Sheet]) -> usize {
    fn walk(t: &Link, seen: &mut HashSet<*const Node>) {
        if let Some(n) = t {
            if seen.insert(Rc::as_ptr(n)) {
                walk(&n.left, seen);
                walk(&n.right, seen);
            }
        }
    }
    let mut seen = HashSet::new();
    for v in versions {
        walk(&v.root, &mut seen);
    }
    seen.len()
}

pub fn node_bytes() -> usize {
    std::mem::size_of::<Node>()
}
