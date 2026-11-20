# capture: session copy=limits_bad.h,users.c,admin.c
gcc -c users.c
gcc -c admin.c
gcc users.o admin.o -o users
