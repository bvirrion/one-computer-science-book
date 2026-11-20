// The checker on hand-made histories, and the protocol's parser and printer.
use store::lincheck::{check, parse_line};
use store::protocol::{parse, parse_reply, Command, Reply};

fn ok(lines: &[&str]) -> bool {
    let ops: Vec<_> = lines.iter().map(|l| parse_line(l).unwrap()).collect();
    check(&ops).values().all(|&v| v)
}

#[test]
fn overlapping_operations_may_take_either_order() {
    assert!(ok(&["1 0 10 a SET x", "2 2 12 a SET y", "1 14 15 a GET x"]));
    assert!(ok(&["1 0 10 a SET x", "2 2 12 a SET y", "1 14 15 a GET y"]));
}

#[test]
fn a_stale_read_is_refused() {
    // y is written after x and acknowledged before the read starts: x cannot be read
    assert!(!ok(&["1 0 1 a SET x", "1 2 3 a SET y", "2 4 5 a GET x"]));
    assert!(!ok(&["1 0 1 a SET x", "2 2 3 a DEL found", "2 4 5 a GET x"]));
}

#[test]
fn an_unanswered_write_may_or_may_not_have_happened() {
    assert!(ok(&["1 0 ? a SET x", "2 5 6 a GET x"]));
    assert!(ok(&["1 0 ? a SET x", "2 5 6 a GET -"]));
    assert!(!ok(&["1 0 ? a SET x", "2 5 6 a GET x", "2 7 8 a GET -"])); // seen, then gone
    assert!(ok(&["1 0 ? a DEL ?", "2 1 2 a SET z", "2 5 6 a GET z"]));
}

#[test]
fn keys_are_checked_on_their_own() {
    let ops: Vec<_> = ["1 0 1 a SET x", "1 2 3 b GET x"]
        .iter()
        .map(|l| parse_line(l).unwrap())
        .collect();
    let result = check(&ops);
    assert!(result["a"]);
    assert!(!result["b"]);
}

#[test]
fn protocol_round_trip() {
    for c in [
        Command::Set("k".into(), "v".into()),
        Command::Get("k".into()),
        Command::Del("k".into()),
        Command::Status,
        Command::Dump,
    ] {
        assert_eq!(parse(&c.to_string()).unwrap(), c);
    }
    for r in [
        Reply::Ok,
        Reply::Value("v".into()),
        Reply::NotFound,
        Reply::Redirect(2),
        Reply::Status("leader".into(), 1),
        Reply::Dump(vec![("a".into(), "1".into())]),
        Reply::Err("no".into()),
    ] {
        assert_eq!(parse_reply(&r.to_string()).unwrap(), r);
    }
    assert_eq!(parse("SET a").unwrap_err(), "SET takes a key and a value");
    assert_eq!(parse("SET a=b 1").unwrap_err(), "a key may not contain =");
    assert_eq!(parse("PUT a 1").unwrap_err(), "unknown command PUT");
}

#[test]
fn exercise_1_lines() {
    assert_eq!(
        Command::Set("ferry".into(), "8h15".into()).to_string() + "\n",
        "SET ferry 8h15\n"
    );
    assert_eq!("SET ferry 8h15\n".len(), 15);
    assert_eq!(parse("SET a=b 1").unwrap_err(), "a key may not contain =");
    assert_eq!(parse("SET a b=c").unwrap(), Command::Set("a".into(), "b=c".into()));
    assert_eq!(parse("GET a b").unwrap_err(), "GET takes one key");
    assert_eq!(parse("DEL  a").unwrap(), Command::Del("a".into()));
    assert_eq!(parse("status").unwrap_err(), "unknown command status");
    assert_eq!(parse("GET").unwrap_err(), "GET takes one key");
    let dump = Reply::Dump(vec![("a".into(), "b=c".into())]);
    assert_eq!(parse_reply(&dump.to_string()).unwrap(), dump);
}

#[test]
fn the_history_of_the_figure() {
    let h = [
        "1 0 4 k SET a",
        "2 2 6 k GET a",
        "3 3 8 k SET b",
        "4 5 ? k DEL ?",
        "2 7 9 k GET b",
    ];
    assert!(ok(&h));
    let with = |extra: &str| ok(&[h.as_slice(), &[extra]].concat());
    assert!(with("1 10 11 k GET -")); // the unanswered DEL took effect after the GET b
    assert!(!with("1 10 11 k GET a")); // a was overwritten by b before this read began
    assert!(with("1 10 11 k GET b")); // the DEL never happened
}
