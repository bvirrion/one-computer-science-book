# capture: session copy=fold.c
gcc -std=c17 -O2 fold.c -o fold
./fold
gcc -std=c17 -O2 -fwrapv fold.c -o fold_wrap
./fold_wrap
