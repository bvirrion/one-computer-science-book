// people_sort.rs: derived orders on the town's people: lexicographic on the fields, in their order.
use std::collections::BTreeMap;

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Person {
    last_name: String, // compared first
    first_name: String,
    birth_year: u32,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone, Copy)]
enum AgeGroup {
    Child, // the smallest: variants compare in the order they are written
    Adult,
    Senior,
}

fn group(p: &Person) -> AgeGroup {
    match 2025 - p.birth_year {
        0..=17 => AgeGroup::Child,
        18..=64 => AgeGroup::Adult,
        _ => AgeGroup::Senior,
    }
}

fn main() {
    let text = std::fs::read_to_string("people.csv").expect("people.csv is in the session");
    let mut people: Vec<Person> = text.lines().skip(1).map(|line| {
        let f: Vec<&str> = line.split(',').collect();
        let year = f[3].parse().unwrap();
        Person { last_name: f[2].into(), first_name: f[1].into(), birth_year: year }
    }).collect();
    people.sort(); // uses the derived Ord
    for p in &people[..3] {
        println!("{} {} {}", p.last_name, p.first_name, p.birth_year);
    }
    people.sort_by_key(|p| (p.birth_year, p.last_name.clone())); // another order, given as a key
    println!("oldest: {} {}", people[0].first_name, people[0].last_name);
    let mut counts = BTreeMap::new(); // keys in the derived order of AgeGroup
    for p in &people {
        *counts.entry(group(p)).or_insert(0) += 1;
    }
    println!("{counts:?}");
}
