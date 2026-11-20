# capture: session copy=library.Makefile,date.h,date.c,date_v0.c,csv.h,csv.c,loans.h,loans.c,loans_main.c,date_test.c,check.h,loans.csv
export LC_ALL=C # hidden
make -f library.Makefile
./checker loans.csv 2025-12-31
for f in date.h date.c csv.h csv.c loans.h loans.c loans_main.c; do touch $f; echo "$f: $(make -f library.Makefile | grep -c -- " -c ")"; done
make -f library.Makefile test
gcc -std=c17 -O0 --coverage -c date.c -o date.o && gcc date_test.c date.o --coverage -o cov_test
./cov_test && gcov -b date.c | sed -n 2,4p
cp date_v0.c date.c
make -f library.Makefile test 2>&1 | grep -v "^gcc"
