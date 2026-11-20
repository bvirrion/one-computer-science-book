// capture: exit
// exo_e0502.rs: the shortest name of a list, then a new name added.
fn main() {
    let mut names = vec![String::from("Mill Row"), String::from("Quay Street")];
    let shortest = names.iter().min_by_key(|n| n.len()).unwrap();
    names.push(String::from("Bridge Way"));
    println!("shortest: {shortest}, {} names", names.len());
}
