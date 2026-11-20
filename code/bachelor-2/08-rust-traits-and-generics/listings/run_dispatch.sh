# capture: session copy=dispatch_cost.rs
rustc --edition 2021 -C opt-level=3 dispatch_cost.rs -o dispatch_cost
./dispatch_cost
./dispatch_cost
