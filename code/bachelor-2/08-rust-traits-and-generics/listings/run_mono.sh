# capture: session copy=mono.rs
rustc --edition 2021 --crate-type lib -C opt-level=1 -C symbol-mangling-version=v0 --emit obj mono.rs
nm -C mono.o | grep -o 'mono::.*' | sort
