// exo_compile.rs: five snippets; build one with --cfg a (or b, c, d, e).
#![allow(unexpected_cfgs, unused)]

#[cfg(a)]
fn snippet() {
    let s = String::from("Mill");
    let t = &s;
    let u = &s;
    println!("{t} {u}");
}

#[cfg(b)]
fn snippet() {
    let mut v = vec![1, 2, 3];
    let first = &v[0];
    v.push(4);
    println!("{first}");
}

#[cfg(c)]
fn snippet() {
    let n = 5;
    let m = n;
    println!("{n} {m}");
}

#[cfg(d)]
fn snippet() {
    let s = String::from("Mill");
    fn calc(s: String) -> usize { s.len() }
    let len = calc(s);
    println!("{s} has {len} bytes");
}

#[cfg(e)]
fn snippet() {
    let mut s = String::from("Mill");
    let r = &mut s;
    r.push_str(" Row");
    let t = &s;
    println!("{t}");
}

fn main() {
    snippet();
}
