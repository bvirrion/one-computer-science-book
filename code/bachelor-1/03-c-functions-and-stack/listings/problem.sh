# capture: session copy=parity_deep.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 parity_deep.c -o parity_O0
{ ./parity_O0; } 2>/dev/null; echo "exit status $?"
gcc -std=c17 -O2 parity_deep.c -o parity_O2
./parity_O2
gcc -std=c17 -O2 -S parity_deep.c -o - | grep -E '(call|jmp)\s+is_' | tr '\t' ' '
