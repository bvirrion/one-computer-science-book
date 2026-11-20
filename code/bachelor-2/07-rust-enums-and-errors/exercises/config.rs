// config.rs: "key = value" lines with comments, and errors that carry their line number (exercise 12).
use std::collections::BTreeMap;
use std::fmt;

#[derive(Debug, PartialEq)]
pub enum Kind {
    NoEquals,
    EmptyKey,
    Duplicate(String),
    BadNumber(String),
}

#[derive(Debug, PartialEq)]
pub struct ConfigError {
    pub line: usize,
    pub kind: Kind,
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &self.kind {
            Kind::NoEquals => write!(f, "line {}: expected key = value", self.line),
            Kind::EmptyKey => write!(f, "line {}: empty key", self.line),
            Kind::Duplicate(k) => write!(f, "line {}: {k} set twice", self.line),
            Kind::BadNumber(v) => write!(f, "line {}: {v:?} is not a number", self.line),
        }
    }
}

/// Every key, with its value; values that look numeric must parse as numbers.
pub fn parse(text: &str) -> Result<BTreeMap<String, String>, ConfigError> {
    let mut map = BTreeMap::new();
    for (i, raw) in text.lines().enumerate() {
        let line = i + 1;
        let err = |kind| ConfigError { line, kind };
        let content = raw.split('#').next().unwrap_or("").trim(); // drop a comment
        if content.is_empty() {
            continue;
        }
        let (k, v) = content.split_once('=').ok_or(err(Kind::NoEquals))?;
        let (k, v) = (k.trim(), v.trim());
        if k.is_empty() {
            return Err(err(Kind::EmptyKey));
        }
        if v.starts_with(|c: char| c.is_ascii_digit() || c == '-')
            && v.parse::<f64>().is_err() {
            return Err(err(Kind::BadNumber(v.to_string())));
        }
        if map.insert(k.to_string(), v.to_string()).is_some() {
            return Err(err(Kind::Duplicate(k.to_string())));
        }
    }
    Ok(map)
}
