# capture: session
cargo build -q --offline --release --manifest-path "$CH/store/Cargo.toml" --target-dir "$HOME/target" # hidden
cp "$HOME/target/release/store" . # hidden
for n in 1 2 3; do (./store node $n --stagger > node$n.log &); done
./store wait-leader
./store send 1 SET x 1
kill -9 $(cat node2/pid)
./store send 3 SET y 2
kill -9 $(cat node3/pid)
./store send 1 SET z 3
./store send 1 GET x
./store send 1 STATUS
kill $(cat node1/pid)
