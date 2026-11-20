//! Tests of chapter 9: the laws, persistence, and the exercises' solutions.
#[path = "../../../exercises/compose.rs"]
pub mod compose;
#[allow(dead_code)]
#[path = "../../../listings/persistent_bst.rs"]
pub mod persistent_bst;
#[allow(dead_code)]
#[path = "../../../listings/persistent_list.rs"]
pub mod persistent_list;
#[path = "../../../exercises/pmap.rs"]
pub mod pmap;
#[path = "../../../exercises/queue.rs"]
pub mod queue;
#[path = "../../../listings/sheet.rs"]
pub mod sheet;
#[path = "../../../exercises/word_freq.rs"]
pub mod word_freq;

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashSet;
    use std::rc::Rc;

    struct Gen(u64);
    impl Gen {
        fn next(&mut self, n: u64) -> u64 {
            self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (self.0 >> 33) % n
        }
        fn list(&mut self) -> Vec<i64> {
            let len = self.next(40);
            (0..len).map(|_| self.next(201) as i64 - 100).collect()
        }
    }

    #[test]
    fn fusion_laws() {
        let mut g = Gen(3);
        let f = |x: i64| x * 3 + 1;
        let h = |x: i64| x.wrapping_mul(x) - 7;
        let p = |x: &i64| x % 3 != 0;
        let q = |x: &i64| *x > -20;
        for _ in 0..500 {
            let xs = g.list();
            // map f . map h = map (f . h)
            let two: Vec<i64> = xs.iter().map(|&x| h(x)).map(f).collect();
            let one: Vec<i64> = xs.iter().map(|&x| f(h(x))).collect();
            assert_eq!(two, one);
            // filter p . filter q = filter (q and p)
            let two: Vec<i64> = xs.iter().copied().filter(q).filter(p).collect();
            let one: Vec<i64> = xs.iter().copied().filter(|x| q(x) && p(x)).collect();
            assert_eq!(two, one);
            // the right fold of cons over nil is the identity
            let back = xs.iter().rev().fold(Vec::new(), |mut acc, &x| {
                acc.insert(0, x);
                acc
            });
            assert_eq!(back, xs);
            // fold of + equals sum, and map then sum equals fold with f inside
            assert_eq!(xs.iter().map(|&x| f(x)).sum::<i64>(), xs.iter().fold(0, |a, &x| a + f(x)));
        }
    }

    #[test]
    fn persistent_list_shares() {
        use persistent_list::*;
        let nil = Rc::new(List::Nil);
        let tail = cons(2, &cons(1, &nil));
        let a = cons(5, &tail);
        assert_eq!(Rc::strong_count(&tail), 2);
        assert_eq!(to_vec(&a), vec![5, 2, 1]);
        drop(a);
        assert_eq!(Rc::strong_count(&tail), 1);
    }

    #[test]
    fn path_copy_counts() {
        use persistent_bst::*;
        let mut g = Gen(11);
        for _ in 0..100 {
            let mut t = None;
            for _ in 0..g.next(50) {
                t = insert(&t, g.next(1000) as i32);
            }
            let mut before = Vec::new();
            keys(&t, &mut before);
            let k = g.next(1000) as i32;
            let t2 = insert(&t, k);
            let mut seen = HashSet::new();
            mark(&t, &mut seen);
            let new = mark(&t2, &mut seen);
            // depth of k in t2 (root depth 0): the number of nodes on its path, minus one
            let mut depth = 0;
            let mut cur = &t2;
            while let Some(n) = cur {
                if n.key == k {
                    break;
                }
                depth += 1;
                cur = if k < n.key { &n.left } else { &n.right };
            }
            if before.contains(&k) {
                assert_eq!(new, depth); // already present: only the path above it is copied
            } else {
                assert_eq!(new, depth + 1); // depth copies and one new leaf
            }
            let mut after = Vec::new();
            keys(&t, &mut after);
            assert_eq!(before, after); // the old version is unchanged
        }
    }

    #[test]
    fn sheet_versions() {
        use sheet::*;
        let cells: Vec<(u32, Cell)> = (0..63).map(|k| (k, Cell::Num(k as f64))).collect();
        let mut cells = cells;
        let sum: Formula = Rc::new(|s: &Sheet| (0..63).map(|k| s.value(k)).sum());
        cells.push((63, Cell::Formula(sum)));
        let mut versions = vec![Sheet::new(&cells)];
        assert_eq!(versions[0].evaluations.get(), 0); // nothing evaluated yet
        for i in 0..200u32 {
            let v = versions.last().unwrap().set(i % 63, Cell::Num(0.0));
            versions.push(v);
        }
        assert_eq!(versions[0].value(63), (0..63).sum::<u32>() as f64);
        assert_eq!(versions[63].value(63), 0.0);
        assert_eq!(versions[0].evaluations.get(), 2);
        let n = 64;
        let bound = n + 200 * (6 + 1);
        assert!(distinct_nodes(&versions) <= bound);
        assert_eq!(distinct_nodes(&versions[..1]), n);
    }

    #[test]
    fn compose_functions() {
        use compose::*;
        let inc_then_double = compose(|x: i32| x * 2, |x: i32| x + 1);
        assert_eq!(inc_then_double(5), 12);
        let len_of_trimmed = compose(|s: &str| s.len(), |s: &'static str| s.trim());
        assert_eq!(len_of_trimmed("  Mill  "), 4);
        let all = compose_all::<i32>(vec![Box::new(|x| x - 3), Box::new(|x| x * x), Box::new(|x| x + 1)]);
        assert_eq!(all(2), 6); // ((2 + 1)^2) - 3
    }

    #[test]
    fn frequencies() {
        let text = "The cat and the hat. THE end, and the end!";
        let top = word_freq::top(text, 3);
        assert_eq!(top, vec![("the".into(), 4), ("and".into(), 2), ("end".into(), 2)]);
        assert_eq!(word_freq::frequencies("").len(), 0);
    }

    #[test]
    fn queue_fifo_and_persistent() {
        let mut q = queue::Queue::new();
        for i in 0..10 {
            q = q.push(i);
        }
        let saved = q.push(10);
        let mut out = Vec::new();
        let mut cur = q;
        while let Some((x, rest, _)) = cur.pop() {
            out.push(x);
            cur = rest;
        }
        assert_eq!(out, (0..10).collect::<Vec<_>>());
        // the saved version still holds everything
        let (x, _, steps) = saved.pop().unwrap();
        assert_eq!((x, steps), (0, 11));
        // reusing the same old version: the reversal is paid again each time
        assert_eq!(saved.pop().unwrap().2, 11);
    }

    #[test]
    fn pmap_old_versions_unchanged() {
        let mut g = Gen(17);
        let mut versions = vec![pmap::PMap::new()];
        let mut truth: Vec<std::collections::BTreeMap<u32, u64>> = vec![Default::default()];
        for i in 0..1000u64 {
            let k = g.next(100) as u32;
            versions.push(versions.last().unwrap().insert(k, i));
            let mut t = truth.last().unwrap().clone();
            t.insert(k, i);
            truth.push(t);
        }
        for (v, t) in versions.iter().zip(&truth).step_by(37) {
            for k in 0..100 {
                assert_eq!(v.get(k), t.get(&k));
            }
        }
    }
}
