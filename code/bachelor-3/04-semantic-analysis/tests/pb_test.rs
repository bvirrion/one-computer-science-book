// The weekend problem's counts.
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "../../02-top-down-parsing/listings/ast.rs"]
mod ast;
#[path = "../../02-top-down-parsing/listings/parser.rs"]
mod parser;
#[path = "../listings/scope.rs"]
mod scope;
#[path = "../listings/resolve.rs"]
mod resolve;
#[path = "../listings/typecheck.rs"]
mod typecheck;
#[path = "../listings/interp.rs"]
mod interp;
#[path = "../exercises/ex5_flat_fixed.rs"]
mod ex5;
#[path = "../exercises/pb_register.rs"]
mod pb;
use pb::Table;

impl Table for ex5::Flat {
    fn enter(&mut self) { ex5::Flat::enter(self) }
    fn exit(&mut self) { ex5::Flat::exit(self) }
    fn declare(&mut self, name: &str) { ex5::Flat::declare(self, name, 0) }
    fn lookup(&mut self, name: &str) -> bool { ex5::Flat::lookup(self, name).is_some() }
}

/// (list comparisons, stack-of-maps probes, map-of-stacks probes)
fn counts(d: usize, m: usize) -> (u64, u64, u64) {
    let src = pb::script(d, m, None);
    std::thread::Builder::new().stack_size(512 << 20).spawn(move || {
        let p = parser::parse_source(&src, "s.moor").unwrap();
        let mut probes = 0;
        let r = resolve::resolve_traced(&p, &mut |_, s| probes = s.probes);
        assert!(r.errors.is_empty());
        let ast::Item::Func(f) = &p.items[0] else { panic!() };
        let mut list = pb::ListScopes::new();
        assert_eq!(pb::walk(&f.body, &mut list), 0);
        let mut flat = ex5::Flat::new();
        assert_eq!(pb::walk(&f.body, &mut flat), 0);
        (list.comparisons, probes, flat.probes)
    }).unwrap().join().unwrap()
}

#[test]
fn the_script_shape() {
    let s = pb::script(2, 2, None);
    assert_eq!(s, "fn main() {\n    var reg = 0;\n    var v1_1 = reg + 1;\n    var v1_2 = reg + 2;\n    {\n        var v2_1 = reg + 1;\n        var v2_2 = reg + 2;\n    }\n}\n");
}

#[test]
fn three_tables() {
    for (d, m) in [(1, 10), (2, 5), (10, 10), (100, 10), (1000, 10), (1, 10_000), (10, 1000), (100, 100)] {
        let n = (d * m) as u64;
        let (list, maps, flat) = counts(d, m);
        assert_eq!(list, n * (n + 1) / 2, "d={d} m={m}");
        assert_eq!(maps, (m * d * (d + 1) / 2) as u64, "d={d} m={m}");
        assert_eq!(flat, n, "d={d} m={m}");
    }
    assert_eq!(counts(1000, 10), (50_005_000, 5_005_000, 10_000));
}

#[test]
fn one_misspelt_block() {
    let src = pb::script(5, 4, Some(3));
    let Err(e) = typecheck::check_source(&src, "s.moor") else { panic!("no error") };
    assert_eq!(e.matches(": error: ").count(), 4);
    assert_eq!(e.matches("'rge' is not declared").count(), 4);
}
