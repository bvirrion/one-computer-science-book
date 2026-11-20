# library.Makefile: the loan checker, in four modules, and the tests of the date module.
CC = gcc
CFLAGS = -std=c17 -O2 -Wall -Wextra -Werror

checker: loans_main.o loans.o csv.o date.o
	$(CC) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

date.o: date.h
csv.o: csv.h
loans.o: loans.h date.h csv.h
loans_main.o: loans.h date.h

date_test: date_test.o date.o
	$(CC) -o $@ $^

date_test.o: date.h check.h

test: date_test
	./date_test

.PHONY: test
