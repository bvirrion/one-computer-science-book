// The weekend problem's numbers (solutions/01-lexical-analysis.tex).
#[path = "../exercises/memo_munch.rs"]
mod memo_munch;
#[path = "../exercises/pb_timetable.rs"]
mod pb_timetable;
#[path = "../listings/regex_nfa.rs"]
mod regex_nfa;
#[path = "../listings/scanner_dfa.rs"]
mod scanner_dfa;

#[test]
fn table_sizes() {
    let (n_nfa, n_big, d) = pb_timetable::build();
    assert_eq!((n_nfa, n_big, d.next.len()), (37, 14, 13));
    assert_eq!(pb_timetable::char_classes(&d), 8);
    let accepting = d.accept.iter().filter(|a| a.is_some()).count();
    assert_eq!(accepting, 9);
}

#[test]
fn a_timetable_line() {
    let (_, _, d) = pb_timetable::build();
    let got = pb_timetable::tokens(&d, "Library 09:45-12:30 room 3");
    let want = [("name", "Library"), ("space", " "), ("time", "09:45"), ("dash", "-"), ("time", "12:30"),
        ("space", " "), ("word", "room"), ("space", " "), ("number", "3")];
    assert_eq!(got.len(), want.len());
    for (g, w) in got.iter().zip(want) {
        assert_eq!((g.0.as_str(), g.1.as_str()), w);
    }
}

#[test]
fn short_inputs() {
    let (_, _, d) = pb_timetable::build();
    assert_eq!(scanner_dfa::scan(&d, b"--->"), Ok((vec![(4, 0, 4)], 4)));
    assert_eq!(scanner_dfa::scan(&d, b"0945"), Ok((vec![(1, 0, 4)], 4)));
    assert_eq!(scanner_dfa::scan(&d, b"12:3x"), Err(2));
    assert_eq!(scanner_dfa::longest(&d, b"12:3x", 0), (Some((2, 1)), 5));
}

#[test]
fn a_rule_line_of_dashes() {
    let (_, _, d) = pb_timetable::build();
    for n in 2..=200usize {
        let line = vec![b'-'; n];
        let (t1, naive) = scanner_dfa::scan(&d, &line).unwrap();
        let (t2, memo) = memo_munch::scan_memo(&d, &line).unwrap();
        assert_eq!(t1, t2);
        assert_eq!(t1.len(), n);
        assert_eq!(naive, n * (n + 1) / 2);
        assert_eq!(memo, 3 * n - 3);
    }
    let line = vec![b'-'; 80];
    assert_eq!(scanner_dfa::scan(&d, &line).unwrap().1, 3240);
    assert_eq!(memo_munch::scan_memo(&d, &line).unwrap().1, 237);
}

#[test]
fn memo_bound_holds_on_mixed_lines() {
    let (_, _, d) = pb_timetable::build();
    let q = d.next.len();
    let mut seed: u64 = 7;
    let pool = ["-", "--", ">", "09:45", "12", " ", "Room", "a", "\n"];
    for _ in 0..500 {
        let mut s = String::new();
        for _ in 0..40 {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            s.push_str(pool[(seed >> 33) as usize % pool.len()]);
        }
        if let (Ok((a, _)), Ok((b, memo))) = (scanner_dfa::scan(&d, s.as_bytes()), memo_munch::scan_memo(&d, s.as_bytes())) {
            assert_eq!(a, b);
            assert!(memo <= (q + 2) * s.len());
        }
    }
}
