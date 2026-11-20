// Exercise 6: CAS key old new, set key to new only if it holds old. It goes through the
// log like SET, so every replica decides it at the same place in the same order.
use std::collections::BTreeMap;

#[derive(Debug, PartialEq)]
enum Command {
    Set(String, String),
    Cas(String, String, String),
}

fn parse(line: &str) -> Result<Command, String> {
    match line.split(' ').filter(|w| !w.is_empty()).collect::<Vec<_>>().as_slice() {
        ["SET", k, v] => Ok(Command::Set(k.to_string(), v.to_string())),
        ["CAS", k, old, new] => Ok(Command::Cas(k.to_string(), old.to_string(), new.to_string())),
        ["CAS", ..] => Err("CAS takes a key, the old value and the new one".to_string()),
        _ => Err("unknown command".to_string()),
    }
}

/// Applied at commit time, in log order: the reply is decided by the replicated map.
fn apply(map: &mut BTreeMap<String, String>, command: &Command) -> String {
    match command {
        Command::Set(k, v) => {
            map.insert(k.clone(), v.clone());
            "OK".to_string()
        }
        Command::Cas(k, old, new) => match map.get(k) {
            Some(v) if v == old => {
                map.insert(k.clone(), new.clone());
                "OK".to_string()
            }
            Some(v) => format!("VALUE {v}"), // refused: the value it found
            None => "NOTFOUND".to_string(),
        },
    }
}

#[test]
fn cas_in_log_order() {
    let log = ["SET seat free", "CAS seat free ada", "CAS seat free bob", "CAS desk free ada"];
    let mut replicas = vec![BTreeMap::new(), BTreeMap::new(), BTreeMap::new()];
    let mut replies = Vec::new();
    for line in log {
        let c = parse(line).unwrap();
        let r: Vec<String> = replicas.iter_mut().map(|m| apply(m, &c)).collect();
        assert!(r.iter().all(|x| *x == r[0])); // every replica gives the same answer
        replies.push(r[0].clone());
    }
    assert_eq!(replies, ["OK", "OK", "VALUE ada", "NOTFOUND"]);
    assert!(replicas.iter().all(|m| m["seat"] == "ada"));
    assert!(parse("CAS seat free").is_err());
}
