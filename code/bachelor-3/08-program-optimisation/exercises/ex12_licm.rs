// ex12_licm.rs -- exercise 12: loop-invariant code motion. An operation in a
// loop whose operands no instruction of the loop writes, into a temporary
// written nowhere else, moves to just before the loop's header label.
#![allow(dead_code)]
use crate::cfg;
use crate::liveness::{def, uses};
use crate::ssa::dominators;
use crate::tac::{FuncTac, Tac};

pub fn hoist(f: &mut FuncTac) -> usize {
    let mut moved = 0;
    loop {
        let g = cfg::build(f);
        let dom = dominators(&g);
        let defs_of = |t: u32, code: &[Tac]| code.iter().filter(|i| def(i) == Some(t)).count();
        let mut found = None;
        'search: for (b, ss) in g.succ.iter().enumerate() {
            for &h in ss.iter().filter(|&&h| dom[b].contains(&h)) {
                // the loop: from the header's start to the back jump's end
                let (start, end) = (g.blocks[h].0, g.blocks[b].1);
                let written: Vec<u32> = f.code[start..end].iter().filter_map(def).collect();
                for k in start..end {
                    let i = &f.code[k];
                    let pure = matches!(i, Tac::Bin(..) | Tac::Neg(..) | Tac::Not(..));
                    let invariant = uses(i).iter().all(|u| !written.contains(u));
                    if pure && invariant && def(i).is_some_and(|d| defs_of(d, &f.code) == 1) {
                        found = Some((k, start));
                        break 'search;
                    }
                }
            }
        }
        let Some((k, header)) = found else {
            return moved;
        };
        let i = f.code.remove(k);
        f.code.insert(header, i);
        moved += 1;
    }
}
