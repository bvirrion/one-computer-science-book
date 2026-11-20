// weather_parse.rs: read the log, keep the good readings, account for every other line.
mod weather;
use weather::{read_log, LogError};

fn main() {
    let path = std::env::args().nth(1).unwrap_or_else(|| "weather.csv".to_string());
    let log = match read_log(&path) {
        Ok(log) => log,
        Err(LogError::Io(e)) => {
            eprintln!("cannot read {path}: {e}");
            std::process::exit(1);
        }
        Err(LogError::NoHeader) => {
            eprintln!("{path}: not a weather log");
            std::process::exit(1);
        }
    };
    println!("{} readings kept", log.readings.len());
    for (line, why) in &log.rejected {
        println!("line {line:>3}: rejected, {why:?}");
    }
    for line in &log.duplicates {
        println!("line {line:>3}: duplicate of an earlier reading");
    }
}
