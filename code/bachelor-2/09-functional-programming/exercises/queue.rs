// queue.rs: a persistent queue made of two persistent lists (exercise 9).
use std::rc::Rc;

#[derive(Debug)]
enum List<T> {
    Nil,
    Cons(T, Rc<List<T>>),
}

fn reverse<T: Clone>(l: &Rc<List<T>>) -> (Rc<List<T>>, usize) {
    let (mut out, mut cur, mut steps) = (Rc::new(List::Nil), l, 0);
    while let List::Cons(x, rest) = cur.as_ref() {
        out = Rc::new(List::Cons(x.clone(), out));
        cur = rest;
        steps += 1;
    }
    (out, steps)
}

/// Elements are taken from front and added to back; back is kept reversed.
#[derive(Debug)]
pub struct Queue<T> {
    front: Rc<List<T>>,
    back: Rc<List<T>>,
}

impl<T: Clone> Queue<T> {
    pub fn new() -> Self {
        Queue { front: Rc::new(List::Nil), back: Rc::new(List::Nil) }
    }

    pub fn push(&self, x: T) -> Self {
        let back = Rc::new(List::Cons(x, Rc::clone(&self.back)));
        Queue { front: Rc::clone(&self.front), back }
    }

    /// The first element, the rest of the queue, and the nodes copied by a reversal.
    pub fn pop(&self) -> Option<(T, Self, usize)> {
        let (front, steps) = match self.front.as_ref() {
            List::Nil => reverse(&self.back), // empty front: the back, reversed
            List::Cons(..) => (Rc::clone(&self.front), 0),
        };
        let back = if steps > 0 { Rc::new(List::Nil) } else { Rc::clone(&self.back) };
        match front.as_ref() {
            List::Nil => None,
            List::Cons(x, rest) => {
                Some((x.clone(), Queue { front: Rc::clone(rest), back }, steps))
            }
        }
    }
}

impl<T: Clone> Default for Queue<T> {
    fn default() -> Self {
        Self::new()
    }
}
