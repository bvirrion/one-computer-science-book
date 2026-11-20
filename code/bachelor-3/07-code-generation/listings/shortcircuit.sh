# capture: session copy=expr.moor
rustc --edition 2021 -O -o moorc $CH/moorc.rs
./moorc expr.moor > expr.S
grep -n -E '^    (b|j )' expr.S
python -m rv run expr.S --stats
