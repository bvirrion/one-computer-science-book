// exo_lazy_order.rs: in which order are the lines printed?
fn main() {
    let v = [1, 2, 3, 4];
    let it = v.iter().inspect(|x| println!("a{x}")).map(|x| x * 10);
    let it = it.inspect(|x| println!("b{x}"));
    println!("start");
    let s: i32 = it.filter(|x| x % 20 == 0).take(1).sum();
    println!("sum {s}");
}
