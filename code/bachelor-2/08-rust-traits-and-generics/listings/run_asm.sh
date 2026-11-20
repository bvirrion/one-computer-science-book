# capture: session copy=units.rs,units_asm.rs
rustc --edition 2021 --crate-type lib -C opt-level=3 --emit obj units_asm.rs
objdump -t units_asm.o | grep -o 'F .text.trip.*'
objdump -d --no-show-raw-insn -M intel --disassemble=trip_speed_raw units_asm.o | grep -P '^ +[0-9a-f]+:' | cut -f2- > body.txt
wc -l < body.txt
grep -c addpd body.txt
tail -3 body.txt
