// ex6_max_test.rs: par_max agrees with the serial maximum for many sizes and p.
#[path = "../exercises/ex6_max.rs"]
mod ex6_max;

#[test]
fn agrees_with_serial_max() {
    let mut x: u64 = 1;
    for n in 0..300 {
        let a: Vec<i64> = (0..n)
            .map(|_| {
                x = x
                    .wrapping_mul(6364136223846793005)
                    .wrapping_add(1442695040888963407);
                (x >> 40) as i64 - (1 << 23)
            })
            .collect();
        for p in 1..=9 {
            assert_eq!(ex6_max::par_max(&a, p), a.iter().copied().max());
        }
    }
    assert_eq!(ex6_max::par_max(&[3, 9, 2], 0), None);
}
