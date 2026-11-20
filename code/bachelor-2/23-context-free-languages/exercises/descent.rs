// descent.rs: a recogniser for S -> T S | c, T -> a S b, one function per nonterminal
// (exercise 7). Each function reads, from the current position, one word of its
// nonterminal; the next letter tells which rule to use.
pub struct Reader<'a> {
    w: &'a [u8],
    pos: usize,
}

impl Reader<'_> {
    fn next_is(&self, c: u8) -> bool {
        self.w.get(self.pos) == Some(&c)
    }

    fn s(&mut self) -> bool {
        if self.next_is(b'c') { // S -> c
            self.pos += 1;
            true
        } else {
            self.next_is(b'a') && self.t() && self.s() // S -> T S: T starts with a
        }
    }

    fn t(&mut self) -> bool {
        self.pos += 1; // the a, checked by the caller
        if !self.s() || !self.next_is(b'b') {
            return false;
        }
        self.pos += 1;
        true
    }
}

pub fn recognise(word: &str) -> bool {
    let mut r = Reader { w: word.as_bytes(), pos: 0 };
    r.s() && r.pos == word.len() // one S, and nothing left over
}
