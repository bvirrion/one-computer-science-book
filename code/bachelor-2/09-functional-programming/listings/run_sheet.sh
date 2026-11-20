# capture: session copy=sheet.rs,sheet_demo.rs
rustc --edition 2021 -O sheet_demo.rs -o sheet_demo
./sheet_demo
