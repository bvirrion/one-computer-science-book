# capture: session
cargo build -q --offline --release --manifest-path "$CH/store/Cargo.toml" --target-dir "$HOME/target" # hidden
cp "$HOME/target/release/store" . # hidden
for n in 1 2 3; do (./store node $n --stagger > node$n.log &); done
./store wait-leader
(./store load history.txt --clients 4 --ops 150 > load.log &)
sleep 0.4; kill -9 $(cat node1/pid)
while ! [ -s load.log ]; do sleep 0.1; done
cat load.log
./store wait-leader
./store check history.txt
wc -l < history.txt
kill $(cat node2/pid node3/pid)
