# capture: session copy=hello.c
gcc -E hello.c -o hello.i
wc -l hello.c hello.i
grep -n 'squared' hello.i
gcc -S -O2 hello.c -o hello.s
sed -n '/^main:/,/ret$/p' hello.s | grep -v cfi
gcc -c -O2 hello.c -o hello.o
file hello.o
nm hello.o
gcc hello.o -o hello
./hello
