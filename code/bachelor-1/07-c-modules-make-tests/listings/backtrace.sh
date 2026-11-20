# capture: session copy=crash.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 -g -fsanitize=address crash.c -o crash
{ ./crash 2>&1 | grep -E "^Riverside|ERROR|caused|#[0-2] "; } 2>/dev/null
