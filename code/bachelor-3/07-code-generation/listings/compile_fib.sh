# capture: session copy=fib.moor
rustc --edition 2021 -O -o moorc $CH/moorc.rs
./moorc fib.moor > fib.S
wc -l fib.S
echo 10 | python -m rv run fib.S --stats
