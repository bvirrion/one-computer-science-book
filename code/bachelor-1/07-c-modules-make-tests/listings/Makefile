# Makefile: build the ratio demo and its tests from separately compiled files.
CC = gcc
CFLAGS = -std=c17 -O2 -Wall -Wextra -Werror

all: ratio_demo ratio_test

ratio_demo: ratio_demo.o ratio.o
	$(CC) -o $@ $^

ratio_test: ratio_test.o ratio.o
	$(CC) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

ratio.o: ratio.h
ratio_demo.o: ratio.h
ratio_test.o: ratio.h check.h

test: ratio_test
	./ratio_test

clean:
	rm -f ratio_demo ratio_test ratio.o ratio_demo.o ratio_test.o

.PHONY: all test clean
