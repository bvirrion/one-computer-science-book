# capture: session copy=loadtest.c,directory.c,directory.h,servers.c,servers.h,net.c,net.h,people.csv,streets.csv
gcc -std=c17 -O2 -Wall -Wextra -o loadtest *.c
./loadtest
