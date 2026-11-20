# Moor, the language compiled across Book 5 Part I (proposal, 2026-11-20)

Named after the series' town (Brenmoor). Small, statically typed, imperative; every
feature is there because a chapter of Part I needs it. **The token set and the AST
are fixed in ch. 1 and ch. 2 and never change afterwards**, so each later chapter
adds modules without editing earlier ones (Rust `#[path = "..."] mod x;` into the
earlier chapter's `listings/`; one source of truth per module).

## Lexical (ch. 1)

- Keywords: `fn var array if else while return true false int bool`.
- Identifiers `[A-Za-z_][A-Za-z0-9_]*`; integers `[0-9]+` (decimal, checked to fit
  32 bits, values wrap as RV32 does); comments `//` to end of line; white space.
- Operators and punctuation: `+ - * / % == != < <= > >= && || ! = ( ) { } [ ] , ; : ->`.
- Every token carries a span (line, column, byte offsets) for error messages.

## Syntax (ch. 2; LL(1) after the transformations the chapter makes)

```
program := item*
item    := "fn" IDENT "(" [param {"," param}] ")" ["->" type] block
         | "var" IDENT ":" type ["=" INT] ";"          (global scalar)
         | "array" IDENT "[" INT "]" ";"                (global int array, zeroed)
param   := IDENT ":" type
type    := "int" | "bool"
block   := "{" stmt* "}"
stmt    := "var" IDENT [":" type] "=" expr ";"
         | IDENT "=" expr ";" | IDENT "[" expr "]" "=" expr ";"
         | "if" expr block ["else" (block | ifstmt)]
         | "while" expr block | "return" [expr] ";" | expr ";" | block
expr    := precedence, loosest first: ||  &&  (== !=)  (< <= > >=)  (+ -)  (* / %)
           prefix - and !; postfix call f(...) and index a[e]; INT, true, false, IDENT, ( expr )
```

`IDENT = expr;` against `expr;` is the chapter's left-factoring example. `&&` and `||`
short-circuit (ch. 7 compiles them to branches).

## Built-ins

`print(e)` (an int, then a newline), `print_char(e)`, `read()` (an int from standard
input). They compile to the RISC-V subset's `ecall` services (ch. 7).

## Semantics (ch. 4)

Block scope, shadowing allowed in an inner block, functions visible everywhere
(mutual recursion), `main()` required with no parameters, returning `int` or nothing.
Types `int` and `bool`, no implicit conversion; a local `var x = e;` gets the type of
`e`. A function with a return type must return on every path (checked).

## The λ-language (ch. 5–6), files `.lam`

`\x. e`, application, `let x = e in e`, `letrec f = \x. e in e`, integers with `+ - *`
and `==`, `<`, booleans, `if e then e else e`, pairs `(e, e)` with `fst`, `snd`.
Interpreted in Rust: small-step and big-step evaluators, the simply typed checker,
then Hindley–Milner inference with let-polymorphism.

## Example

```
// fib.moor
fn fib(n: int) -> int {
    if n < 2 { return n; }
    return fib(n - 1) + fib(n - 2);
}
fn main() {
    var i = 0;
    while i < 10 { print(fib(i)); i = i + 1; }
}
```
