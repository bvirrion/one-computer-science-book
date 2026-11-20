// capture: exit
// longest_scope.rs: the result of longest used after one of its arguments is dropped.
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() >= y.len() { x } else { y }
}

fn main() {
    let a = String::from("Orchard Way");
    let result;
    {
        let b = String::from("Mill Row");
        result = longest(&a, &b);
    }
    println!("{result}");
}
