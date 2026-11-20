# capture: session copy=write_text.c,write_binary.c fixtimes
gcc -std=c17 -O2 -Wall write_text.c -o write_text && ./write_text
gcc -std=c17 -O2 -Wall write_binary.c -o write_binary && ./write_binary
ls -l numbers.txt numbers.bin
od -A d -t x1 numbers.txt
od -A d -t x1 numbers.bin
od -A d -t d4 numbers.bin
