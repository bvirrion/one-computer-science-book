// protocol.rs: the commands a client sends, the replies, and the parser.
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Command {
    Set(String, String),
    Get(String),
    Del(String),
    Count,
    Quit,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Reply {
    Ok,
    Value(String),
    NotFound,
    Count(usize),
    Err(String),
}

pub const MAX_LINE: usize = 1024;

/// One line, without its newline, to a command, or the reason it is not one.
pub fn parse(line: &str) -> Result<Command, String> {
    if line.len() > MAX_LINE {
        return Err(format!("line longer than {MAX_LINE} bytes"));
    }
    let (word, rest) = line.split_once(' ').unwrap_or((line, ""));
    let args: Vec<&str> = rest.split(' ').filter(|a| !a.is_empty()).collect();
    match (word, args.as_slice()) {
        ("", _) => Err("empty line".to_string()),
        ("SET", [key, value]) => Ok(Command::Set(key.to_string(), value.to_string())),
        ("GET", [key]) => Ok(Command::Get(key.to_string())),
        ("DEL", [key]) => Ok(Command::Del(key.to_string())),
        ("COUNT", []) => Ok(Command::Count),
        ("QUIT", []) => Ok(Command::Quit),
        ("SET", _) => Err("SET takes a key and a value".to_string()),
        ("GET" | "DEL", _) => Err(format!("{word} takes one key")),
        ("COUNT" | "QUIT", _) => Err(format!("{word} takes no argument")),
        _ => Err(format!("unknown command {word}")),
    }
}

impl fmt::Display for Command {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Command::Set(k, v) => write!(f, "SET {k} {v}"),
            Command::Get(k) => write!(f, "GET {k}"),
            Command::Del(k) => write!(f, "DEL {k}"),
            Command::Count => write!(f, "COUNT"),
            Command::Quit => write!(f, "QUIT"),
        }
    }
}

impl fmt::Display for Reply {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Reply::Ok => write!(f, "OK"),
            Reply::Value(v) => write!(f, "VALUE {v}"),
            Reply::NotFound => write!(f, "NOTFOUND"),
            Reply::Count(n) => write!(f, "COUNT {n}"),
            Reply::Err(reason) => write!(f, "ERR {reason}"),
        }
    }
}
