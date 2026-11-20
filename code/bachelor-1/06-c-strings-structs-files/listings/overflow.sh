# capture: session copy=overflow.c,overflow_local.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
export LC_ALL=C # hidden
gcc -std=c17 -O0 overflow.c -o plain && ./plain
gcc -std=c17 -O0 -g -fsanitize=address overflow.c -o asan && ./asan
gcc -std=c17 -O0 -g -fsanitize=address overflow_local.c -o local
{ ./local 2>&1 | grep -E "ERROR|WRITE of|#1 |overflows"; } 2>/dev/null
gcc -std=c17 -O2 overflow.c -o fortified 2>/dev/null
{ ./fortified 2>&1; } 2>/dev/null; echo "exit status $?"
