// weather.rs: the weather stations' log, one Result per line.
use std::collections::HashSet;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Station {
    Hilltop,
    Riverside,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Reading {
    pub date: String, // YYYY-MM-DD
    pub station: Station,
    pub temp_c: f64,
    pub rain_mm: f64,
    pub wind_kmh: f64,
}

#[derive(Debug, PartialEq)]
pub enum LineError {
    FieldCount(usize),
    UnknownStation(String),
    Missing(&'static str),                             // an empty field
    BadNumber { field: &'static str, text: String },   // not a number
    ErrorCode { field: &'static str },                 // -99.0, the code for "no measurement"
}

fn number(field: &'static str, text: &str) -> Result<f64, LineError> {
    if text.is_empty() {
        return Err(LineError::Missing(field));
    }
    let v: f64 = text.parse()
        .map_err(|_| LineError::BadNumber { field, text: text.to_string() })?;
    if v == -99.0 {
        return Err(LineError::ErrorCode { field });
    }
    Ok(v)
}

pub fn parse_line(line: &str) -> Result<Reading, LineError> {
    let f: Vec<&str> = line.split(',').collect();
    if f.len() != 5 {
        return Err(LineError::FieldCount(f.len()));
    }
    let station = match f[1] {
        "Hilltop" => Station::Hilltop,
        "Riverside" => Station::Riverside,
        other => return Err(LineError::UnknownStation(other.to_string())),
    };
    Ok(Reading {
        date: f[0].to_string(),
        station,
        temp_c: number("temp_c", f[2])?, // ? : on the first bad field, return its error
        rain_mm: number("rain_mm", f[3])?,
        wind_kmh: number("wind_kmh", f[4])?,
    })
}

#[derive(Debug)]
pub enum LogError {
    Io(std::io::Error), // the file could not be read
    NoHeader,
}

impl From<std::io::Error> for LogError {
    fn from(e: std::io::Error) -> Self {
        LogError::Io(e) // lets ? turn an io::Error into a LogError
    }
}

pub struct Log {
    pub readings: Vec<Reading>,
    pub rejected: Vec<(usize, LineError)>, // (line number, why)
    pub duplicates: Vec<usize>,            // line numbers of repeated (date, station) pairs
}

pub fn read_log(path: &str) -> Result<Log, LogError> {
    let text = std::fs::read_to_string(path)?; // an io::Error becomes a LogError here
    let mut lines = text.lines();
    if lines.next() != Some("date,station,temp_c,rain_mm,wind_kmh") {
        return Err(LogError::NoHeader);
    }
    let mut log = Log { readings: Vec::new(), rejected: Vec::new(), duplicates: Vec::new() };
    let mut seen = HashSet::new();
    for (i, line) in lines.enumerate() {
        let number = i + 2; // the header is line 1
        match parse_line(line) {
            Ok(r) if !seen.insert((r.date.clone(), r.station)) => log.duplicates.push(number),
            Ok(r) => log.readings.push(r),
            Err(e) => log.rejected.push((number, e)),
        }
    }
    Ok(log)
}
