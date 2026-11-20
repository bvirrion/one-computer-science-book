# capture: session copy=units.rs,units_mix.rs exit
rustc --edition 2021 -O units.rs -o units && ./units
rustc --edition 2021 units_mix.rs 2>&1 | grep -E '^(error|  -->)'
