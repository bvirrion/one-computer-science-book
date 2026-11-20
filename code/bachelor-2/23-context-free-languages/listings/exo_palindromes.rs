// exo_palindromes.rs: a grammar for the palindromes over a, b, checked up to length 12
// (exercise 3).
#[allow(dead_code)]
mod grammar;

fn main() {
    let g = grammar::Grammar::parse("P -> a P a | b P b | a | b | ε");
    let made = g.generated(12);
    let mut all = 0;
    for n in 0..=12 {
        for m in 0..1u32 << n {
            let w: String = (0..n).map(|i| if m >> i & 1 == 0 { 'a' } else { 'b' }).collect();
            let palindrome = w.chars().eq(w.chars().rev());
            assert_eq!(made.contains(&w), palindrome, "{w}");
            all += palindrome as usize;
        }
    }
    println!("{all} palindromes up to length 12, all generated, and nothing else");
}
