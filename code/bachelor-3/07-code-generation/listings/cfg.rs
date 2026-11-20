// cfg.rs -- basic blocks and the control-flow graph of a function's
// three-address code.
#![allow(dead_code)]
use crate::tac::{FuncTac, Tac};

pub struct Cfg {
    pub blocks: Vec<(usize, usize)>, // [start, end) in the code
    pub succ: Vec<Vec<usize>>,
}

/// A leader starts a block: the first instruction, every label, and
/// every instruction that follows a jump, a branch or a return.
pub fn leaders(code: &[Tac]) -> Vec<usize> {
    let mut ls = vec![];
    for (i, ins) in code.iter().enumerate() {
        let after_transfer =
            i > 0 && matches!(code[i - 1], Tac::Jump(_) | Tac::Branch(..) | Tac::Ret(_));
        if i == 0 || matches!(ins, Tac::Label(_)) || after_transfer {
            ls.push(i);
        }
    }
    ls
}

pub fn build(f: &FuncTac) -> Cfg {
    let ls = leaders(&f.code);
    let ends = ls.iter().skip(1).copied().chain([f.code.len()]);
    let blocks: Vec<(usize, usize)> = ls.iter().copied().zip(ends).collect();
    let block_of_label =
        |l: u32| blocks.iter().position(|&(s, _)| f.code[s] == Tac::Label(l)).unwrap();
    let mut succ = vec![];
    for (k, &(_, end)) in blocks.iter().enumerate() {
        let next = if k + 1 < blocks.len() { vec![k + 1] } else { vec![] };
        succ.push(match &f.code[end - 1] {
            Tac::Jump(l) => vec![block_of_label(*l)],
            Tac::Branch(.., l) => {
                let target = block_of_label(*l);
                let fall: Vec<usize> = next.into_iter().filter(|&n| n != target).collect();
                [vec![target], fall].concat() // taken, then fall through
            }
            Tac::Ret(_) => vec![], // to the exit
            _ => next,
        });
    }
    Cfg { blocks, succ }
}
