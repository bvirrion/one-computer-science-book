# capture: session copy=transpose_bug.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 -g -fsanitize=address transpose_bug.c -o transpose_bug
./transpose_bug
