// word_freq.rs: word frequencies with one fold into a map (exercise 7).
use std::collections::HashMap;

pub fn frequencies(text: &str) -> HashMap<String, u32> {
    text.split(|c: char| !c.is_alphanumeric())
        .filter(|w| !w.is_empty())
        .map(|w| w.to_lowercase())
        .fold(HashMap::new(), |mut m, w| {
            *m.entry(w).or_insert(0) += 1;
            m
        })
}

/// The k most frequent words, ties broken alphabetically.
pub fn top(text: &str, k: usize) -> Vec<(String, u32)> {
    let mut v: Vec<(String, u32)> = frequencies(text).into_iter().collect();
    v.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0)));
    v.into_iter().take(k).collect()
}
