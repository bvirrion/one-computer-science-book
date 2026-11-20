# capture: session copy=Makefile,ratio.h,ratio.c,ratio_demo.c,ratio_test.c,check.h
export LC_ALL=C # hidden
make
make
touch ratio_demo.c
make
touch ratio.h
make
make test
make clean
