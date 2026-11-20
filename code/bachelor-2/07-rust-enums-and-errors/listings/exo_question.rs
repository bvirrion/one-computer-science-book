// exo_question.rs: where does each call return? Predict the four lines.
fn parse_pages(s: &str) -> Result<u32, String> {
    let n: u32 = s.trim().parse().map_err(|_| format!("not a number: {s:?}"))?;
    if n == 0 {
        return Err("a book has pages".to_string());
    }
    Ok(n)
}

fn total(a: &str, b: &str) -> Result<u32, String> {
    let x = parse_pages(a)?;
    println!("  first is {x}");
    let y = parse_pages(b)?;
    println!("  second is {y}");
    Ok(x + y)
}

fn main() {
    println!("{:?}", total("65", " 133"));
    println!("{:?}", total("sixty", "133"));
    println!("{:?}", total("65", "0"));
}
