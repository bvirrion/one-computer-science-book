// eliminate.rs: from the DFA of the binary multiples of 3 back to an expression.
#[allow(dead_code)]
mod dfa;
#[allow(dead_code)]
mod regex;

fn main() {
    let three = dfa::Dfa { alphabet: vec!['0', '1'], accept: vec![true, false, false],
                           delta: vec![vec![0, 1], vec![2, 0], vec![1, 2]] }; // r -> 2r + c
    let re = dfa::eliminate(&three);
    println!("expression: {}", re.show());
    let m = regex::Matcher::new(&regex::glushkov(&re));
    let ok = (0u32..4096).all(|x| m.matches(&format!("{x:b}")) == (x % 3 == 0));
    println!("matches exactly the multiples of 3 among 0 .. 4095: {ok}");
}
