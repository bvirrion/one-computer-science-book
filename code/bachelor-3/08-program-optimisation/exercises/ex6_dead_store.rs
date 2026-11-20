// ex6_dead_store.rs -- exercise 6: a store to a global that is overwritten
// later in the same block, with no load of it and no call in between, is dead.
#![allow(dead_code)]
use crate::cfg;
use crate::tac::{FuncTac, Tac};

pub fn dead_stores(f: &mut FuncTac) -> usize {
    let g = cfg::build(f);
    let mut keep = vec![true; f.code.len()];
    for &(s, e) in &g.blocks {
        for k in s..e {
            let Tac::StoreG(name, _) = &f.code[k] else {
                continue;
            };
            for i in &f.code[k + 1..e] {
                match i {
                    Tac::LoadG(_, x) if x == name => break, // read: the store is needed
                    Tac::Call(..) => break,                 // the callee may read it
                    Tac::StoreG(x, _) if x == name => {
                        keep[k] = false;
                        break;
                    }
                    _ => {}
                }
            }
        }
    }
    let before = f.code.len();
    let mut it = keep.iter();
    f.code.retain(|_| *it.next().unwrap());
    before - f.code.len()
}
