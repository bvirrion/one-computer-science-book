# capture: session
cargo build -q --offline --release --manifest-path "$CH/store/Cargo.toml" --target-dir "$HOME/target" # hidden
cp "$HOME/target/release/store" . # hidden
for n in 1 2 3; do (./store node $n --stagger > node$n.log &); done
./store wait-leader
for n in 1 2 3; do ./store send $n STATUS; done
./store send 3 SET ferry 8h15
./store send 2 GET ferry
./store caught-up 3
./store dump 3
cat node1.log node2.log node3.log
kill $(cat node1/pid node2/pid node3/pid)
