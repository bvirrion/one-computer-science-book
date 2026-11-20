# capture: session copy=billing.moor
rustc --edition 2021 -O -o color_demo $CH/color_demo.rs
./color_demo billing.moor 7 6 | sed -n '/^interference/,$p'
