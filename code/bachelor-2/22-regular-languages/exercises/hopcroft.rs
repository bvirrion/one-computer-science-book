// hopcroft.rs: Hopcroft's minimisation: split by the smaller half (exercise 11).
use crate::dfa::Dfa;
use std::collections::HashSet;

/// The class of each state in the minimal automaton, numbered from state 0's.
pub fn hopcroft(d: &Dfa) -> Vec<usize> {
    let (n, k) = (d.delta.len(), d.alphabet.len());
    let mut inv = vec![vec![vec![]; n]; k]; // inv[a][q]: the states that go to q on a
    for p in 0..n {
        for a in 0..k {
            inv[a][d.delta[p][a]].push(p);
        }
    }
    let (acc, rej): (Vec<usize>, Vec<usize>) = (0..n).partition(|&q| d.accept[q]);
    let mut blocks: Vec<Vec<usize>> =
        [acc, rej].into_iter().filter(|b| !b.is_empty()).collect();
    let mut block_of = vec![0; n];
    for (i, b) in blocks.iter().enumerate() {
        b.iter().for_each(|&q| block_of[q] = i);
    }
    let smaller = (0..blocks.len()).min_by_key(|&i| blocks[i].len()).unwrap();
    let mut work: HashSet<(usize, usize)> = (0..k).map(|a| (smaller, a)).collect();
    let mut hit = vec![false; n]; // marks, cleared after each splitter
    while let Some(&(b, a)) = work.iter().next() {
        work.remove(&(b, a));
        let mut entering: Vec<usize> = blocks[b].iter() // the states entering b on a
            .flat_map(|&q| inv[a][q].iter().copied()).collect();
        entering.iter().for_each(|&p| hit[p] = true);
        entering.sort_by_key(|&p| block_of[p]);
        let mut touched: Vec<usize> = entering.iter().map(|&p| block_of[p]).collect();
        touched.dedup();
        for y in touched {
            let (inside, outside): (Vec<usize>, Vec<usize>) =
                blocks[y].iter().partition(|&&q| hit[q]);
            if outside.is_empty() {
                continue; // y lies entirely in the preimage: no split
            }
            let z = blocks.len(); // y keeps `inside`, the new block z gets `outside`
            outside.iter().for_each(|&q| block_of[q] = z);
            let small = if inside.len() <= outside.len() { y } else { z };
            blocks[y] = inside;
            blocks.push(outside);
            for c in 0..k {
                if work.contains(&(y, c)) {
                    work.insert((z, c)); // both halves still to be used
                } else {
                    work.insert((small, c)); // the smaller half is enough
                }
            }
        }
        entering.iter().for_each(|&p| hit[p] = false);
    }
    let mut number = vec![usize::MAX; blocks.len()];
    let mut next = 0;
    (0..n).map(|q| {
        if number[block_of[q]] == usize::MAX {
            number[block_of[q]] = next;
            next += 1;
        }
        number[block_of[q]]
    }).collect()
}
