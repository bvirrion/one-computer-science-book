# capture: session
cargo build -q --offline --release --manifest-path "$CH/store/Cargo.toml" --target-dir "$HOME/target" # hidden
cp "$HOME/target/release/store" . # hidden
(./store node 1 --nodes 1 > node1.log &)
./store wait-leader --nodes 1
exec 3<>/dev/tcp/127.0.0.1/24321
printf 'SET colour red\nGET colour\nDEL colour\nGET colour\nPUT colour blue\nSET colour\n' >&3
head -n 6 <&3
./store send 1 SET town Kelsford --nodes 1
./store send 1 GET town --nodes 1
cat node1.log
kill $(cat node1/pid)
