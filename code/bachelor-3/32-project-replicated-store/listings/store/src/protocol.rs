// protocol.rs: one command per line from a client, one reply per line back.
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Command {
    Set(String, String),
    Get(String),
    Del(String),
    Status, // which role this node has, and which node it thinks leads
    Dump,   // this node's applied map, for checking a replica
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Reply {
    Ok,
    Value(String),
    NotFound,
    Redirect(u32), // ask node n, the leader as far as this node knows
    Status(String, u32), // role, leader (0 = none known)
    Dump(Vec<(String, String)>),
    Err(String),
}

pub const MAX_LINE: usize = 1024;

/// One line, without its newline, to a command, or the reason it is not one.
pub fn parse(line: &str) -> Result<Command, String> {
    if line.len() > MAX_LINE {
        return Err(format!("line longer than {MAX_LINE} bytes"));
    }
    let words: Vec<&str> = line.split(' ').filter(|w| !w.is_empty()).collect();
    if words.get(1).is_some_and(|key| key.contains('=')) {
        return Err("a key may not contain =".to_string()); // DUMP prints key=value
    }
    match words.as_slice() {
        [] => Err("empty line".to_string()),
        ["SET", key, value] => Ok(Command::Set(key.to_string(), value.to_string())),
        ["GET", key] => Ok(Command::Get(key.to_string())),
        ["DEL", key] => Ok(Command::Del(key.to_string())),
        ["STATUS"] => Ok(Command::Status),
        ["DUMP"] => Ok(Command::Dump),
        ["SET", ..] => Err("SET takes a key and a value".to_string()),
        ["GET" | "DEL", ..] => Err(format!("{} takes one key", words[0])),
        ["STATUS" | "DUMP", ..] => Err(format!("{} takes no argument", words[0])),
        [word, ..] => Err(format!("unknown command {word}")),
    }
}

impl fmt::Display for Command {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Command::Set(k, v) => write!(f, "SET {k} {v}"),
            Command::Get(k) => write!(f, "GET {k}"),
            Command::Del(k) => write!(f, "DEL {k}"),
            Command::Status => write!(f, "STATUS"),
            Command::Dump => write!(f, "DUMP"),
        }
    }
}

impl fmt::Display for Reply {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Reply::Ok => write!(f, "OK"),
            Reply::Value(v) => write!(f, "VALUE {v}"),
            Reply::NotFound => write!(f, "NOTFOUND"),
            Reply::Redirect(n) => write!(f, "REDIRECT {n}"),
            Reply::Status(role, leader) => write!(f, "STATUS {role} {leader}"),
            Reply::Dump(pairs) => {
                write!(f, "DUMP")?;
                pairs.iter().try_for_each(|(k, v)| write!(f, " {k}={v}"))
            }
            Reply::Err(reason) => write!(f, "ERR {reason}"),
        }
    }
}

/// A reply line back to a reply; the client's side of `Display`.
pub fn parse_reply(line: &str) -> Result<Reply, String> {
    let (word, rest) = line.split_once(' ').unwrap_or((line, ""));
    let number =
        |s: &str| s.parse::<u32>().map_err(|_| format!("bad number in {line:?}"));
    match word {
        "OK" if rest.is_empty() => Ok(Reply::Ok),
        "VALUE" => Ok(Reply::Value(rest.to_string())),
        "NOTFOUND" if rest.is_empty() => Ok(Reply::NotFound),
        "REDIRECT" => Ok(Reply::Redirect(number(rest)?)),
        "STATUS" => match rest.split_once(' ') {
            Some((role, leader)) => {
                Ok(Reply::Status(role.to_string(), number(leader)?))
            }
            None => Err(format!("bad status {line:?}")),
        },
        "DUMP" => Ok(Reply::Dump(
            rest.split(' ')
                .filter_map(|kv| kv.split_once('='))
                .map(|(k, v)| (k.to_string(), v.to_string()))
                .collect(),
        )),
        "ERR" => Ok(Reply::Err(rest.to_string())),
        _ => Err(format!("unknown reply {line:?}")),
    }
}
