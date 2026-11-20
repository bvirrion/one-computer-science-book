// typestate.rs: the state of a connection as a type parameter: send only when open (exercise 12).
use std::marker::PhantomData;

pub struct Closed;
pub struct Open;

pub struct Connection<State> {
    pub sent: Vec<String>,
    _state: PhantomData<State>, // no data: the state lives only in the type
}

impl Connection<Closed> {
    pub fn new() -> Self {
        Connection { sent: Vec::new(), _state: PhantomData }
    }
    pub fn open(self) -> Connection<Open> {
        Connection { sent: self.sent, _state: PhantomData } // consumes the closed connection
    }
}

impl Default for Connection<Closed> {
    fn default() -> Self {
        Self::new()
    }
}

impl Connection<Open> {
    pub fn send(&mut self, msg: &str) {
        self.sent.push(msg.to_string());
    }
    pub fn close(self) -> Connection<Closed> {
        Connection { sent: self.sent, _state: PhantomData }
    }
}
