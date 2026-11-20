# capture: session copy=sum_to.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 sum_to.c -o sum_O0
{ ./sum_O0; } 2>/dev/null; echo "exit status $?"
gcc -std=c17 -O2 sum_to.c -o sum_O2
./sum_O2; echo "exit status $?"
