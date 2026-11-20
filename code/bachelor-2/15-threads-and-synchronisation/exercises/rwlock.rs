//! A readers-writers lock that prefers writers (exercise 9).
use std::sync::{Condvar, Mutex};

#[derive(Default)]
struct State {
    readers: usize,        // readers inside
    writer: bool,          // a writer inside
    writers_waiting: usize,
}

#[derive(Default)]
pub struct RwLockW {
    state: Mutex<State>,
    changed: Condvar,
}

impl RwLockW {
    pub fn read_lock(&self) {
        let mut s = self.state.lock().unwrap();
        while s.writer || s.writers_waiting > 0 {   // a waiting writer goes first
            s = self.changed.wait(s).unwrap();
        }
        s.readers += 1;
    }

    pub fn read_unlock(&self) {
        let mut s = self.state.lock().unwrap();
        s.readers -= 1;
        if s.readers == 0 {
            self.changed.notify_all();
        }
    }

    pub fn write_lock(&self) {
        let mut s = self.state.lock().unwrap();
        s.writers_waiting += 1;
        while s.writer || s.readers > 0 {
            s = self.changed.wait(s).unwrap();
        }
        s.writers_waiting -= 1;
        s.writer = true;
    }

    pub fn write_unlock(&self) {
        let mut s = self.state.lock().unwrap();
        s.writer = false;
        self.changed.notify_all();
    }
}
