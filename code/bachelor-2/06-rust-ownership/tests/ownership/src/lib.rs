//! Tests of chapter 6: the listings' functions and the exercises' solutions.
#[path = "../../../listings/dict_table.rs"]
pub mod dict_table;
#[path = "../../../exercises/distinct.rs"]
pub mod distinct;
#[path = "../../../exercises/first_word.rs"]
pub mod first_word;
#[path = "../../../listings/longest.rs"]
pub mod longest;
#[path = "../../../exercises/reverse_words.rs"]
pub mod reverse_words;
#[path = "../../../listings/slices.rs"]
pub mod slices;
#[path = "../../../exercises/split.rs"]
pub mod split;
#[path = "../../../exercises/stack.rs"]
pub mod stack;

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[test]
    fn longest_and_first_letter() {
        assert_eq!(longest::longest("Mill Row", "Quay"), "Mill Row");
        assert_eq!(longest::longest("ab", "cd"), "ab"); // ties: the first
        assert_eq!(longest::first_letter("Café"), "C");
        assert_eq!(longest::first_letter("é"), "é");
        assert_eq!(longest::first_letter(""), "");
    }

    #[test]
    fn slices_total() {
        let pages = [65, 133, 412, 98, 251];
        assert_eq!(slices::total(&pages[1..4]), 643);
        assert_eq!(slices::total(&pages), 959);
        assert_eq!(slices::total(&[]), 0);
    }

    #[test]
    fn first_word_cases() {
        assert_eq!(first_word::first_word("Mill Lane"), "Mill");
        assert_eq!(first_word::first_word("Café\tLane"), "Café");
        assert_eq!(first_word::first_word("Quay"), "Quay");
        assert_eq!(first_word::first_word(" lead"), "");
    }

    #[test]
    fn halves() {
        let mut v = vec![1, 2, 3, 10, 20, 30];
        split::add_halves(&mut v);
        assert_eq!(v, [1, 2, 3, 11, 22, 33]);
        let mut odd = vec![1, 2, 10, 20, 30]; // mid = 2: the second half is longer
        split::add_halves(&mut odd);
        assert_eq!(odd, [1, 2, 11, 22, 30]);
        let mut w = vec![3, 9, 4, 9];
        split::largest_first(&mut w);
        assert_eq!(w, [9, 9, 4, 3]); // max_by_key picks the last of equal largest
        let mut empty: Vec<i32> = vec![];
        split::largest_first(&mut empty);
    }

    #[test]
    fn reversed_words() {
        let s = String::from("Café on Mill Lane");
        let p = s.as_ptr();
        let r = reverse_words::reverse_words(s);
        assert_eq!(r, "Lane Mill on Café");
        assert_eq!(r.as_ptr(), p); // the same buffer
        assert_eq!(reverse_words::reverse_words(String::from("über straße")), "straße über");
        assert_eq!(reverse_words::reverse_words(String::new()), "");
    }

    #[test]
    fn stack_against_vec() {
        let mut s = stack::Stack::default();
        let mut v = Vec::new();
        let mut x: u64 = 7;
        for _ in 0..10_000 {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(1);
            if x >> 62 == 0 {
                assert_eq!(s.pop(), v.pop());
            } else {
                s.push(x);
                v.push(x);
            }
            assert_eq!(s.peek(), v.last());
            assert_eq!(s.len(), v.len());
        }
        if let Some(top) = s.peek_mut() {
            *top = 1;
            assert_eq!(s.peek(), Some(&1));
        }
        let mut long = stack::Stack::default();
        for i in 0..1_000_000 {
            long.push(i); // dropped by the loop of Drop, not by a recursion a million deep
        }
        assert!(!long.is_empty());
    }

    #[test]
    fn distinct_versions() {
        let names: Vec<String> = (0..300).map(|i| format!("Street {}", (i * 7) % 120)).collect();
        let a = distinct::distinct(&names);
        let b = distinct::distinct_fast(&names);
        assert_eq!(a, b);
        assert_eq!(a.len(), 120);
        assert_eq!(a[1], "Street 7"); // the order of first appearance
    }

    #[test]
    fn dict_against_hashmap() {
        let mut d = dict_table::Dict::default();
        let mut reference: HashMap<String, u32> = HashMap::new();
        let mut x: u64 = 2025;
        for _ in 0..50_000 {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            let w = format!("w{}", (x >> 33) % 3000);
            *d.count(&w) += 1;
            *reference.entry(w).or_insert(0) += 1;
        }
        assert_eq!(d.len(), reference.len());
        for (w, c) in d.iter() {
            assert_eq!(reference[w.as_str()], c);
        }
        let titles = std::fs::read_to_string("../../../../../data/town/books.csv").unwrap();
        let mut t = dict_table::Dict::default();
        for line in titles.lines().skip(1) {
            for w in line.split(',').nth(1).unwrap().split(' ') {
                *t.count(w) += 1;
            }
        }
        assert_eq!(t.len(), 34);
        assert_eq!(*t.count("The"), 42);
    }
}
