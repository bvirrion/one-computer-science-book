// stack.rs: a stack as a chain of boxed nodes (exercise 10).
struct Node<T> {
    value: T,
    next: Option<Box<Node<T>>>, // the node owns the rest of the chain
}

pub struct Stack<T> {
    head: Option<Box<Node<T>>>,
    len: usize,
}

impl<T> Default for Stack<T> {
    fn default() -> Self {
        Stack { head: None, len: 0 }
    }
}

impl<T> Stack<T> {
    pub fn push(&mut self, value: T) {
        let next = self.head.take(); // move the old chain out, leaving None
        self.head = Some(Box::new(Node { value, next }));
        self.len += 1;
    }

    pub fn pop(&mut self) -> Option<T> {
        let node = self.head.take()?; // we now own the top node
        self.head = node.next;
        self.len -= 1;
        Some(node.value)
    }

    pub fn peek(&self) -> Option<&T> {
        self.head.as_ref().map(|n| &n.value)
    }

    pub fn peek_mut(&mut self) -> Option<&mut T> {
        self.head.as_mut().map(|n| &mut n.value)
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }
}

impl<T> Drop for Stack<T> {
    fn drop(&mut self) {
        // a loop, not the default recursion: a long chain would overflow the call stack
        let mut cur = self.head.take();
        while let Some(mut node) = cur {
            cur = node.next.take();
        }
    }
}
