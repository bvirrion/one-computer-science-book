# capture: session copy=billing.moor,billing_counts.py,loans.csv
rustc --edition 2021 -O -o moorc_opt $CH/moorc_opt.rs
./moorc_opt -O0 billing.moor > O0.S
./moorc_opt -O1 billing.moor > O1.S
for k in 12 6 5 4 3 2 1; do ./moorc_opt -O2 -k $k billing.moor > k$k.S; done
python billing_counts.py loans.csv O0.S O1.S k12.S k6.S k5.S k4.S k3.S k2.S k1.S
