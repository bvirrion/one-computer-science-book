// capture: exit
// exo_fnmut.rs: count the late loans with a helper that applies a function to each loan.
fn for_each_loan(days: &[u32], f: impl Fn(u32)) {
    for &d in days {
        f(d);
    }
}

fn main() {
    let days = [3, 25, 30, 12, 22];
    let mut late = 0;
    for_each_loan(&days, |d| {
        if d > 21 {
            late += 1;
        }
    });
    println!("{late} late");
}
