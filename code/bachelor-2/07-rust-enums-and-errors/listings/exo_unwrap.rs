// capture: exit
// exo_unwrap.rs: reading "street,number" lines; the program stops on the third.
fn main() {
    // print a panic without the thread's number, which changes at each run
    std::panic::set_hook(Box::new(|p| {
        eprintln!("panicked at {}:\n{}", p.location().unwrap(), p.payload_as_str().unwrap_or("?"))
    }));
    let lines = ["Mill Lane,12", "Quay Street,3", "Bridge Way", "Castle Row,8"];
    let mut sum = 0;
    for line in lines {
        let (street, number) = line.split_once(',').unwrap();
        let n: u32 = number.parse().unwrap();
        println!("{street}: {n}");
        sum += n;
    }
    println!("sum {sum}");
}
