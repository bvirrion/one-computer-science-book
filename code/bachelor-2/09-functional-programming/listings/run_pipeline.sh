# capture: session copy=pipeline.rs,weather.csv
rustc --edition 2021 -O pipeline.rs -o pipeline
./pipeline
