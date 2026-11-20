// capture: exit
// exo_twice.rs: the number of long titles, then their list.
fn main() {
    let titles = ["The Silent Code", "Seven Comets", "The Paper Forest", "Harbour Lights"];
    let long = titles.iter().filter(|t| t.len() > 13);
    println!("{} long titles", long.count());
    for t in long {
        println!("{t}");
    }
}
