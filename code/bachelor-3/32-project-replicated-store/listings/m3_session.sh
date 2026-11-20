# capture: session
cargo build -q --offline --release --manifest-path "$CH/store/Cargo.toml" --target-dir "$HOME/target" # hidden
cp "$HOME/target/release/store" . # hidden
./store trace 3 --ticks 200
./store sim --runs 1000 --ticks 400 --loss 50 --crash 2
