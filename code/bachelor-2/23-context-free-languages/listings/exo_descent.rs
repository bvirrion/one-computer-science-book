// exo_descent.rs: the hand-written recogniser against the grammar on every word of length
// at most 9 over a, b, c (exercise 7).
#[allow(dead_code)]
mod grammar;
#[path = "../exercises/descent.rs"]
mod descent;

fn main() {
    let g = grammar::Grammar::parse("S -> T S | c\nT -> a S b");
    let language = g.generated(9);
    let (mut words, mut layer) = (vec![String::new()], vec![String::new()]);
    for _ in 0..9 { // the words of length 1, 2, ... 9, one layer at a time
        layer = layer.iter().flat_map(|w| ["a", "b", "c"].map(|c| format!("{w}{c}")))
            .collect();
        words.extend(layer.iter().cloned());
    }
    let differ = |w: &&String| descent::recognise(w) != language.contains(*w);
    let wrong = words.iter().filter(differ).count();
    println!("{} words tried, {} in the language, {wrong} disagreements", words.len(),
             language.len());
    println!("the words of the language up to length 9: {language:?}");
}
