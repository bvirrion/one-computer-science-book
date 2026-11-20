# capture: session copy=fib.c
gcc --version | head -n 1
gcc -S -O1 -fno-asynchronous-unwind-tables -fcf-protection=none -o fib.s fib.c
grep -vE '^\s+\.|^[0-9]+:' fib.s | expand -t 8
