# capture: session copy=count.h,count.c,report.c,wcmain.c
gcc -E count.c | wc -l
gcc -c count.c report.c wcmain.c
nm count.o
nm report.o
nm wcmain.o
size count.o report.o wcmain.o
gcc count.o report.o wcmain.o -o wcount
printf 'one two\nthree four five\n' | ./wcount
