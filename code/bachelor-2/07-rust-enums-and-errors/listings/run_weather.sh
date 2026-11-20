# capture: session copy=weather.rs,weather_parse.rs,weather.csv exit
rustc --edition 2021 -O weather_parse.rs -o weather_parse
./weather_parse weather.csv
./weather_parse wether.csv
