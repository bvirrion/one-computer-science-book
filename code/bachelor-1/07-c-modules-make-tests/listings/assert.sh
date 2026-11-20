# capture: session copy=assert_demo.c
export LC_ALL=C # hidden
gcc -std=c17 -O2 assert_demo.c -o assert_demo
{ ./assert_demo 2>&1; } 2>/dev/null; echo "exit status $?"
gcc -std=c17 -O2 -DNDEBUG assert_demo.c -o assert_demo
./assert_demo; echo "exit status $?"
