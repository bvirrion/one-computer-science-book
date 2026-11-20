// exo_min_bug.rs: refining an incomplete automaton by its defined successors (exercise 6).
use std::collections::HashMap;

fn main() {
    // {ab, ba}: 0 -a-> 1, 0 -b-> 2, 1 -b-> 3, 2 -a-> 3; 3 accepts; None: no transition
    let delta = [[Some(1), Some(2)], [None, Some(3)], [Some(3), None], [None, None]];
    let accept = [false, false, false, true];
    let mut class: Vec<usize> = accept.iter().map(|&a| a as usize).collect();
    loop {
        let mut seen = HashMap::new();
        let next: Vec<usize> = (0..4).map(|q| {
            // the bug: the classes of the successors that exist, without their letters
            let key: Vec<usize> = std::iter::once(class[q])
                .chain(delta[q].iter().flatten().map(|&r| class[r])).collect();
            let n = seen.len();
            *seen.entry(key).or_insert(n)
        }).collect();
        if next.iter().max() == class.iter().max() {
            break;
        }
        class = next;
    }
    println!("classes: {class:?}");
    for w in ["ab", "ba", "aa", "bb"] {
        let mut q = Some(0);
        for c in w.chars() {
            let a = if c == 'a' { 0 } else { 1 };
            // run on the merged automaton: any member of the class may move
            q = q.and_then(|q| (0..4).filter(|&p| class[p] == class[q])
                .find_map(|p| delta[p][a]));
        }
        println!("{w}: {}", q.is_some_and(|q| accept[q]));
    }
}
