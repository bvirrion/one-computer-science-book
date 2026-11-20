# capture: session copy=exo_assert.c
export LC_ALL=C # hidden
gcc -std=c17 -O2 exo_assert.c -o exo_assert
{ ./exo_assert 2>&1; } 2>/dev/null; echo "exit status $?"
