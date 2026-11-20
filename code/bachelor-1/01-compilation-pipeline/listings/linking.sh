# capture: session copy=square.h,square.c,main.c,twice.c
gcc -c square.c
gcc -c main.c
nm square.o
nm main.o
gcc main.o square.o -o squares
./squares
gcc main.o -o broken
gcc -c twice.c
gcc main.o square.o twice.o -o broken
