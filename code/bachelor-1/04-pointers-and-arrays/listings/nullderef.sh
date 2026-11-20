# capture: session copy=nullderef.c
gcc -std=c17 -O2 -Wall -Wextra nullderef.c -o nullderef
{ ./nullderef; } 2>/dev/null; echo "exit status $?"
