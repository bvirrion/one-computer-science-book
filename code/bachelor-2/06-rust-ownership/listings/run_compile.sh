# capture: session copy=exo_compile.rs
for s in a b c d e; do echo "$s: $(rustc --edition 2021 --cfg $s exo_compile.rs 2>&1 | grep -m1 '^error\[' || echo compiles)"; done
