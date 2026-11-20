# capture: session copy=measure.py
cp $CH/../../07-code-generation/listings/*.moor . # hidden
rustc --edition 2021 -O -o moorc_opt $CH/moorc_opt.rs
for p in fib sum_array primes; do for O in 0 1 2; do ./moorc_opt -O$O $p.moor > $p.$O.S; done; done
python measure.py fib:20 sum_array primes
