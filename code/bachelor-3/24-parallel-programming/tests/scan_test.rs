// scan_test.rs: both scans of scan.rs and the blocked scan of weather_scan.rs agree
// with a running sum, and the counted work and span follow their formulas.
#[allow(dead_code)]
#[path = "../listings/scan.rs"]
mod scan;
#[allow(dead_code)]
#[path = "../listings/weather_scan.rs"]
mod weather_scan;

fn data(n: usize, seed: u64) -> Vec<i64> {
    let mut x = seed;
    (0..n)
        .map(|_| {
            x = x
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            (x >> 50) as i64 - 4000
        })
        .collect()
}

#[test]
fn scans_are_right_and_counted() {
    for k in 0..12u32 {
        let n = 1usize << k;
        let a = data(n, k as u64 + 1);
        let (inc, hw, hs) = scan::hillis_steele(&a);
        let mut ex = a.clone();
        let (bw, bs) = scan::blelloch(&mut ex, false);
        let mut run = 0;
        for i in 0..n {
            assert_eq!(ex[i], run);
            run += a[i];
            assert_eq!(inc[i], run);
        }
        assert_eq!(bw, 2 * (n as u64 - 1));
        assert_eq!(bs, 2 * k);
        assert_eq!(hw, (n * k as usize - (n - 1)) as u64);
        assert_eq!(hs, k);
    }
}

#[test]
fn blocked_scan_is_right() {
    for n in [0, 1, 2, 7, 64, 1000, 4097] {
        let a = data(n, n as u64 + 3);
        let mut want = vec![0; n];
        weather_scan::scan_seq(&a, &mut want);
        for p in 1..=9 {
            let mut got = vec![0; n];
            weather_scan::scan_par(&a, &mut got, p);
            assert_eq!(got, want, "n = {n}, p = {p}");
        }
    }
}
