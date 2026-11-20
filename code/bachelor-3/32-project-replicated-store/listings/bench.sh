# capture: session
cargo build -q --offline --release --manifest-path "$CH/store/Cargo.toml" --target-dir "$HOME/target" # hidden
cp "$HOME/target/release/store" . # hidden
for b in "" --batch; do (./store node 1 --nodes 1 --base 24340 --dir single $b > single.log &); ./store bench --nodes 1 --base 24340 --clients 16 --seconds 3; kill $(cat single/pid); sleep 0.3; done
for n in 1 2 3; do (./store node $n --stagger > node$n.log &); done
./store bench --clients 16 --seconds 3
kill $(cat node1/pid node2/pid node3/pid); sleep 0.3
for n in 1 2 3; do (./store node $n --stagger --batch --dir batch$n > batch$n.log &); done
./store bench --clients 16 --seconds 3
kill $(cat batch1/pid batch2/pid batch3/pid)
