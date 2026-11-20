// list.rs: the linked list as a recursive enum (exercise 9).
#[derive(Debug, Clone, PartialEq)]
pub enum List<T> {
    Nil,
    Cons(T, Box<List<T>>),
}
use List::*;

impl<T> List<T> {
    pub fn from_vec(v: Vec<T>) -> List<T> {
        v.into_iter().rev().fold(Nil, |rest, x| Cons(x, Box::new(rest)))
    }

    pub fn len(&self) -> usize {
        let mut n = 0;
        let mut cur = self;
        while let Cons(_, rest) = cur {
            n += 1;
            cur = rest; // a loop, not a recursion: no stack growth
        }
        n
    }

    pub fn is_empty(&self) -> bool {
        matches!(self, Nil)
    }

    pub fn rev(self) -> List<T> {
        let mut out = Nil;
        let mut cur = self;
        while let Cons(x, rest) = cur {
            out = Cons(x, Box::new(out)); // move each node's value to the front of out
            cur = *rest;
        }
        out
    }

    pub fn map<U>(&self, f: impl Fn(&T) -> U) -> List<U> {
        match self {
            Nil => Nil,
            Cons(x, rest) => Cons(f(x), Box::new(rest.map(f))),
        }
    }
}
