# capture: session copy=dict.h,dict_bench.c,dict_table.rs,dict_bench.rs
gcc -std=c17 -O2 dict_bench.c -o bench_c
rustc --edition 2021 -C opt-level=2 dict_bench.rs -o bench_rs
for i in 1 2 3; do ./bench_c; ./bench_rs; done
