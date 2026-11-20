// pipeline.rs: the mean temperature of each station, as one pipeline per station.
fn main() {
    let text = std::fs::read_to_string("weather.csv").expect("weather.csv is in the session");
    for station in ["Hilltop", "Riverside"] {
        let (sum, n) = text
            .lines()
            .skip(1)                                              // the header
            .map(|line| line.split(',').collect::<Vec<&str>>())
            .filter(|f| f[1] == station)
            .filter_map(|f| f[2].parse::<f64>().ok())             // empty fields fail to parse
            .filter(|&t| t != -99.0)                              // the stations' error code
            .fold((0.0, 0), |(s, n), t| (s + t, n + 1));
        println!("{station:<10} {n} readings, mean {:.2}", sum / n as f64);
    }
}
