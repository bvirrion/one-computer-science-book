# capture: session
cargo build -q --offline --release --manifest-path "$CH/store/Cargo.toml" --target-dir "$HOME/target" # hidden
cp "$HOME/target/release/store" . # hidden
for n in 1 2 3; do (./store node $n --stagger > node$n.log &); done
./store wait-leader
for k in a b c d e; do ./store send 1 SET $k 1 > /dev/null; done
kill -9 $(cat node1/pid)
./store wait-leader
./store send 3 GET c
./store send 3 SET f 2
(./store node 1 --stagger >> node1.log &)
./store caught-up 1
./store dump 1
cat node1.log node2.log node3.log
kill $(cat node1/pid node2/pid node3/pid)
