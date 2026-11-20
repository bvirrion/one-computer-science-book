# capture: session copy=exo_fwrite.c
gcc -std=c17 -O2 exo_fwrite.c -o exo_fwrite && ./exo_fwrite
od -A d -t x1 x.bin
