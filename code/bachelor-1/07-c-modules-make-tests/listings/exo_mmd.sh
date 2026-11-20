# capture: session copy=mmd.Makefile,date.h,date.c,csv.h,csv.c,loans.h,loans.c,loans_main.c
export LC_ALL=C # hidden
make -f mmd.Makefile
cat loans.d
touch csv.h
make -f mmd.Makefile
