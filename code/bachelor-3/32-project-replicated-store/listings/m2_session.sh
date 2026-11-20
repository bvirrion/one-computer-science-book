# capture: session
cargo build -q --offline --release --manifest-path "$CH/store/Cargo.toml" --target-dir "$HOME/target" # hidden
cp "$HOME/target/release/store" . # hidden
(./store node 1 --nodes 1 > node1.log &)
./store wait-leader --nodes 1
./store send 1 SET bridge open --nodes 1
./store send 1 SET bridge closed --nodes 1
od -A d -t x1 -w16 node1/wal.log | head -n 6
stat -c %s node1/wal.log
kill $(cat node1/pid); sleep 0.2
truncate -s -5 node1/wal.log
(./store node 1 --nodes 1 >> node1.log &)
./store wait-leader --nodes 1
./store send 1 GET bridge --nodes 1
stat -c %s node1/wal.log
cat node1.log
kill $(cat node1/pid)
