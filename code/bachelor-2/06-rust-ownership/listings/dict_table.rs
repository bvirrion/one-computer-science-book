// dict_table.rs: the word counter of dict.h in Rust: open addressing, linear probing, grown at half full.
pub struct Dict {
    slots: Vec<Option<(String, u32)>>, // None: an empty slot; the table owns every word
    len: usize,
}

fn hash(s: &str) -> u64 {
    // FNV-1a, 64 bits, as in dict.h
    s.bytes().fold(14695981039346656037, |h, b| (h ^ b as u64).wrapping_mul(1099511628211))
}

impl Default for Dict {
    fn default() -> Self {
        Dict { slots: vec![None; 8], len: 0 }
    }
}

impl Dict {
    fn find(&self, word: &str) -> usize {
        let mask = self.slots.len() - 1;
        let mut i = hash(word) as usize & mask;
        while let Some((w, _)) = &self.slots[i] {
            if w == word {
                break;
            }
            i = (i + 1) & mask;
        }
        i
    }

    fn grow(&mut self) {
        let bigger = vec![None; 2 * self.slots.len()];
        let old = std::mem::replace(&mut self.slots, bigger); // the old slots, now ours to empty
        for (w, c) in old.into_iter().flatten() {
            let i = self.find(&w); // the String moves into its new slot: no copy of the bytes
            self.slots[i] = Some((w, c));
        }
    }

    /// The counter of `word`, created at 0 if missing; the table stays borrowed while used.
    pub fn count(&mut self, word: &str) -> &mut u32 {
        let mut i = self.find(word);
        if self.slots[i].is_none() {
            if 2 * (self.len + 1) > self.slots.len() {
                self.grow();
                i = self.find(word);
            }
            self.slots[i] = Some((word.to_string(), 0)); // the table's own copy
            self.len += 1;
        }
        &mut self.slots[i].as_mut().unwrap().1
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn iter(&self) -> impl Iterator<Item = (&String, u32)> {
        self.slots.iter().flatten().map(|(w, c)| (w, *c))
    }
}
