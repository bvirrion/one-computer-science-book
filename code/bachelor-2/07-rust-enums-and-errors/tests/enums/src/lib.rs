//! Tests of chapter 7: the weather log, the trees, and the exercises' solutions.
#[path = "../../../listings/bst.rs"]
pub mod bst;
#[path = "../../../exercises/checked.rs"]
pub mod checked;
#[path = "../../../exercises/config.rs"]
pub mod config;
#[path = "../../../exercises/diff.rs"]
pub mod diff;
#[path = "../../../listings/expr.rs"]
pub mod expr;
#[path = "../../../exercises/json.rs"]
pub mod json;
#[path = "../../../exercises/list.rs"]
pub mod list;
#[path = "../../../exercises/monthly.rs"]
pub mod monthly;
#[path = "../../../listings/weather.rs"]
pub mod weather;

/// The mirror image of a tree (exercise 8), for the property mirror(mirror(t)) == t.
pub fn mirror(t: &bst::Tree) -> bst::Tree {
    match t {
        bst::Tree::Leaf => bst::Tree::Leaf,
        bst::Tree::Node(l, k, r) => bst::Tree::Node(Box::new(mirror(r)), *k, Box::new(mirror(l))),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    struct Gen(u64); // a small deterministic generator for the property tests
    impl Gen {
        fn next(&mut self, n: u64) -> u64 {
            self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (self.0 >> 33) % n
        }
    }

    const LOG: &str = "../../../../../data/town/weather.csv";

    #[test]
    fn every_planted_defect() {
        use weather::LineError::*;
        let log = weather::read_log(LOG).unwrap();
        assert_eq!(log.readings.len(), 722);
        let missing = log.rejected.iter().filter(|(_, e)| *e == Missing("temp_c")).count();
        let codes = log.rejected.iter().filter(|(_, e)| *e == ErrorCode { field: "temp_c" }).count();
        assert_eq!((missing, codes, log.rejected.len()), (6, 2, 8));
        assert_eq!(log.duplicates, vec![332]);
        assert_eq!(log.readings.len() + log.rejected.len() + log.duplicates.len(), 731); // every line
        assert!(log.readings.iter().all(|r| r.temp_c > -40.0 && r.temp_c < 50.0));
    }

    #[test]
    fn parse_line_errors() {
        use weather::{parse_line, LineError::*};
        assert_eq!(parse_line("2025-01-01,Hilltop,3.9,0.0"), Err(FieldCount(4)));
        assert_eq!(parse_line("2025-01-01,Harbour,3.9,0.0,1"), Err(UnknownStation("Harbour".into())));
        assert_eq!(parse_line("2025-01-01,Hilltop,3.9,,1"), Err(Missing("rain_mm")));
        assert_eq!(parse_line("2025-01-01,Hilltop,warm,0,1"),
                   Err(BadNumber { field: "temp_c", text: "warm".into() }));
        assert!(parse_line("2025-01-01,Hilltop,-0.0,0,1").is_ok());
        assert!(matches!(weather::read_log("no_such_file.csv"), Err(weather::LogError::Io(_))));
    }

    #[test]
    fn monthly_tree() {
        let log = weather::read_log(LOG).unwrap();
        let tree = monthly::monthly(&log.readings);
        assert_eq!(tree.len(), 24);
        let total: u32 = tree.values().map(|a| a.n).sum();
        assert_eq!(total, 722);
        let june = tree[&(weather::Station::Riverside, 6)];
        assert_eq!(june.n, 30); // the duplicate counted once
        assert!(june.min <= june.mean() && june.mean() <= june.max);
        let keys: Vec<_> = tree.keys().copied().collect();
        assert!(keys.windows(2).all(|w| w[0] < w[1]));
    }

    fn random_expr(g: &mut Gen, depth: u32) -> expr::Expr {
        use expr::Expr::*;
        match if depth == 0 { g.next(2) } else { g.next(4) } {
            0 => Num(g.next(5) as i64 - 1), // often 0 or 1, to exercise the rules
            1 => X,
            2 => Add(Box::new(random_expr(g, depth - 1)), Box::new(random_expr(g, depth - 1))),
            _ => Mul(Box::new(random_expr(g, depth - 1)), Box::new(random_expr(g, depth - 1))),
        }
    }

    #[test]
    fn simplify_preserves_eval() {
        let mut g = Gen(1);
        for _ in 0..3000 {
            let e = random_expr(&mut g, 6);
            let s = e.clone().simplify();
            for x in [-3, 0, 1, 2, 7, i64::MAX] {
                assert_eq!(e.eval(x), s.eval(x), "{e} became {s}");
            }
            assert_eq!(s.clone().simplify(), s); // simplifying twice changes nothing
        }
    }

    #[test]
    fn tree_properties() {
        let mut g = Gen(5);
        for _ in 0..200 {
            let mut t = bst::Tree::default();
            let mut keys: Vec<i32> = (0..g.next(60)).map(|_| g.next(100) as i32).collect();
            for &k in &keys {
                t.insert(k);
            }
            keys.sort();
            keys.dedup();
            let mut walk = Vec::new();
            t.in_order(&mut walk);
            assert_eq!(walk, keys); // the in-order walk is sorted, without repeats
            assert!(t.height() <= keys.len());
            assert!((0..100).all(|k| t.contains(k) == keys.binary_search(&k).is_ok()));
            assert_eq!(mirror(&mirror(&t)), t);
        }
    }

    #[test]
    fn checked_and_mean() {
        assert_eq!(checked::checked_div(7, 2), Some(3));
        assert_eq!(checked::checked_div(-7, 2), Some(-3));
        assert_eq!(checked::checked_div(1, 0), None);
        assert_eq!(checked::checked_div(i32::MIN, -1), None);
        assert_eq!(checked::mean(&[]), None);
        assert_eq!(checked::mean(&[1.0, 2.0, 6.0]), Some(3.0));
    }

    #[test]
    fn json_printer() {
        use json::Json::*;
        let v = Obj(vec![
            ("title".into(), Str("The \"Silent\" Code".into())),
            ("pages".into(), Num(65.0)),
            ("tags".into(), Arr(vec![Str("mystery".into()), Null, Bool(true)])),
        ]);
        assert_eq!(v.to_text(), r#"{"title":"The \"Silent\" Code","pages":65,"tags":["mystery",null,true]}"#);
        assert_eq!(Arr(vec![]).to_text(), "[]");
        assert_eq!(Str("a\\b\n".into()).to_text(), r#""a\\b\n""#);
    }

    #[test]
    fn list_operations() {
        let l = list::List::from_vec(vec![1, 2, 3]);
        assert_eq!(l.len(), 3);
        assert_eq!(l.map(|x| x * 10), list::List::from_vec(vec![10, 20, 30]));
        assert_eq!(l.clone().rev(), list::List::from_vec(vec![3, 2, 1]));
        assert_eq!(l.clone().rev().rev(), l);
        assert!(list::List::<i32>::Nil.is_empty());
        let long = list::List::from_vec((0..10_000).collect::<Vec<u32>>());
        assert_eq!(long.len(), 10_000);
        let back = long.rev(); // in a loop: no recursion
        assert_eq!(back.len(), 10_000);
    }

    fn random_f(g: &mut Gen, depth: u32) -> diff::F {
        use diff::F::*;
        let b = Box::new;
        match if depth == 0 { g.next(2) } else { g.next(6) } {
            0 => Num(g.next(4) as f64 - 1.0),
            1 => X,
            2 => Add(b(random_f(g, depth - 1)), b(random_f(g, depth - 1))),
            3 => Mul(b(random_f(g, depth - 1)), b(random_f(g, depth - 1))),
            4 => Sin(b(random_f(g, depth - 1))),
            _ => Cos(b(random_f(g, depth - 1))),
        }
    }

    #[test]
    fn derivative_numerically() {
        let mut g = Gen(9);
        for _ in 0..500 {
            let f = random_f(&mut g, 4);
            let d = f.derive().simplify();
            for x in [-1.3, -0.2, 0.4, 1.1, 2.5] {
                let h = 1e-5;
                let numeric = (f.eval(x + h) - f.eval(x - h)) / (2.0 * h);
                let exact = d.eval(x);
                assert!((numeric - exact).abs() <= 1e-4 * (1.0 + exact.abs()), "{f:?} at {x}");
            }
            assert!(d.size() <= f.derive().size()); // simplification never grows
        }
    }

    #[test]
    fn config_errors() {
        use config::{parse, ConfigError, Kind};
        let ok = parse("# town server\nport = 44071\nname = Riverside  # the station\n\n").unwrap();
        assert_eq!(ok["port"], "44071");
        assert_eq!(ok["name"], "Riverside");
        assert_eq!(parse("a = 1\nb 2"), Err(ConfigError { line: 2, kind: Kind::NoEquals }));
        assert_eq!(parse(" = 1"), Err(ConfigError { line: 1, kind: Kind::EmptyKey }));
        assert_eq!(parse("a = 1\n\na = 2"), Err(ConfigError { line: 3, kind: Kind::Duplicate("a".into()) }));
        let e = parse("rate = 1.2.3").unwrap_err();
        assert_eq!(e.to_string(), "line 1: \"1.2.3\" is not a number");
    }
}
