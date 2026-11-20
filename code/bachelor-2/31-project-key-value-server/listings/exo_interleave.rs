// exo_interleave.rs (exercise 5): clients a and b, unlocked, each GET x then SET x to it + 1.
// Every interleaving of the four steps, and the final value of x (it starts at 0).

fn run(order: &[usize]) -> i64 {
    let (mut x, mut read, mut step) = (0, [0i64; 2], [0usize; 2]);
    for &c in order {
        if step[c] == 0 { read[c] = x } else { x = read[c] + 1 }
        step[c] += 1;
    }
    x
}

fn main() {
    let mut orders = Vec::new();
    for first_b in 0..4 {
        for second_b in first_b + 1..4 {
            let mut order = vec![0; 4];
            order[first_b] = 1;
            order[second_b] = 1;
            orders.push(order);
        }
    }
    for order in &orders {
        let names: Vec<String> = order.iter().scan([0, 0], |step, &c| {
            step[c] += 1;
            Some(format!("{}{}", ["GET", "SET"][step[c] - 1], ["b", "a"][c]))
        }).collect();
        println!("{:<28} x = {}", names.join(" "), run(order));
    }
}
