// persistent_list.rs: immutable lists that share their tails, counted by Rc.
use std::rc::Rc;

#[derive(Debug)]
pub enum List {
    Nil,
    Cons(i32, Rc<List>), // Rc: shared ownership, freed when the last owner goes
}
use List::*;

pub fn cons(x: i32, rest: &Rc<List>) -> Rc<List> {
    Rc::new(Cons(x, Rc::clone(rest))) // clones the pointer, not the list: count + 1
}

pub fn to_vec(l: &List) -> Vec<i32> {
    let mut out = Vec::new();
    let mut cur = l;
    while let Cons(x, rest) = cur {
        out.push(*x);
        cur = rest;
    }
    out
}

#[allow(dead_code)]
fn main() {
    let nil = Rc::new(Nil);
    let tail = cons(3, &cons(2, &cons(1, &nil)));          // 3, 2, 1
    let a = cons(10, &tail);                                // 10, 3, 2, 1
    let b = cons(20, &tail);                                // 20, 3, 2, 1
    println!("a = {:?}, b = {:?}", to_vec(&a), to_vec(&b));
    println!("owners of tail: {}", Rc::strong_count(&tail)); // tail itself, a, b
    drop(a);
    println!("after dropping a: {}", Rc::strong_count(&tail));
    println!("tail unchanged: {:?}", to_vec(&tail));
}
