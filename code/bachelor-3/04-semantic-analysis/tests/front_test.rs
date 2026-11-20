// Tests of resolution, type checking and the interpreter.
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

fn errors(src: &str) -> Vec<String> {
    match typecheck::check_source(src, "t.moor") {
        Ok(_) => vec![],
        Err(e) => e.lines().filter(|l| l.starts_with("t.moor:")).map(|l| l.splitn(4, ':').nth(3).unwrap().trim().to_string()).collect(),
    }
}
fn run(src: &str, input: &[i32]) -> (String, Result<i32, String>) {
    let (p, _, _) = typecheck::check_source(src, "t.moor").unwrap();
    let o = interp::run(&p, input, 100_000);
    (o.output, o.exit)
}

#[test]
fn samples() {
    assert!(errors(&std::fs::read_to_string("../listings/ok.moor").unwrap()).is_empty());
    let e = errors(&std::fs::read_to_string("../listings/errors.moor").unwrap());
    assert_eq!(e.len(), 6); // four errors, two of them with a note
    assert_eq!(run(&std::fs::read_to_string("../listings/ok.moor").unwrap(), &[]).0, "3\n1\n");
    let (out, exit) = run(&std::fs::read_to_string("../listings/sieve.moor").unwrap(), &[]);
    assert_eq!(out.lines().count(), 15);
    assert_eq!(exit, Ok(15));
}

#[test]
fn exercise_2_type_errors() {
    let e = errors("fn f(a: int) -> bool { return a; }\nfn main() { var b = f(1) + 2; if 3 { print(true); } while f(0) == 1 { } }");
    assert_eq!(e, vec![
        "error: the returned value must be a bool, found an int",
        "error: the left operand of '+' must be an int, found a bool",
        "error: the condition of an if must be a bool, found an int",
        "error: argument 1 of 'print' must be an int, found a bool",
        "error: '==' compares a bool with an int",
    ]);
}

#[test]
fn absorbing_error_type() {
    // one cause, one message: zz is unknown, and nothing above it complains
    assert_eq!(errors("fn main() { var y = (zz + 1) * 2 < 3 && true; print(y); }"),
               vec!["error: 'zz' is not declared", "error: argument 1 of 'print' must be an int, found a bool"]);
    assert_eq!(errors("fn main() { var y = !(zz * 2 > 1); }"), vec!["error: 'zz' is not declared"]);
}

#[test]
fn scopes_and_shadowing() {
    let src = "fn main() { var x = 1; { var x = true; if x { print(2); } } print(x); }";
    assert!(errors(src).is_empty());
    assert_eq!(run(src, &[]).0, "2\n1\n");
    assert_eq!(errors("fn main() { var x = x + 1; }"), vec!["error: 'x' is not declared"]);
    assert_eq!(errors("fn g() {} fn main() { g = 1; }"), vec!["error: 'g' is a function, not a variable"]);
    assert_eq!(errors("fn print(n: int) {} fn main() {}"), vec!["error: 'print' is the name of a built-in function"]);
}

#[test]
fn return_on_every_path() {
    assert!(errors("fn f(n: int) -> int { if n > 0 { return 1; } else { return 2; } } fn main() {}").is_empty());
    assert_eq!(errors("fn f(n: int) -> int { while true { return 1; } } fn main() {}").len(), 1);
    assert!(errors("fn f(n: int) -> int { { return 1; } } fn main() {}").is_empty());
}

#[test]
fn arithmetic_is_rv32() {
    let (out, _) = run("fn main() { print(2147483647 + 1); print(7 / 0); print(-7 % 0); print(-7 / 2); print(-7 % 2); }", &[]);
    assert_eq!(out, "-2147483648\n-1\n-7\n-3\n-1\n");
    let (out, exit) = run("array a[3]; fn main() { a[2] = read(); print(a[2]); a[3] = 1; }", &[42]);
    assert_eq!(out, "42\n");
    assert_eq!(exit, Err("index 3 is out of range for 'a', of size 3".into()));
}

#[test]
fn exercise_9_recursive_output() {
    let (out, exit) = run(&std::fs::read_to_string("../exercises/ex9.moor").unwrap(), &[]);
    assert_eq!(out, "1\n2\n0\n3\n1\n4\n1\n2\n0\n");
    assert_eq!(exit, Ok(3));
}

#[test]
fn exercise_1_and_4_scopes() {
    let src = "var x: int = 1;\nfn show() { print(x); }\nfn main() { var x = 2; show(); }";
    assert_eq!(run(src, &[]).0, "1\n"); // static scope: show sees the global
    let src = "var n: int = 1;\nfn f(n: int) -> int {\n    var m = n;\n    {\n        var n = m + 1;\n        m = n;\n    }\n    return n + m;\n}\nfn main() { print(f(5)); }";
    assert!(errors(src).is_empty());
    assert_eq!(run(src, &[]).0, "11\n");
}
