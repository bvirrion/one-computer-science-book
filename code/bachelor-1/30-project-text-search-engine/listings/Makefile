# Makefile: the search engine, the naive scan, the measurement and the unit tests.
CC = gcc
CFLAGS = -std=c17 -O2 -Wall -Wextra -Werror
LDLIBS = -lm
CORE = tokenize.o folder.o index.o query.o topk.o

all: search naive measure units_test

search: main.o $(CORE)
	$(CC) -o $@ $^ $(LDLIBS)
naive: naive.o scan.o $(CORE)
	$(CC) -o $@ $^ $(LDLIBS)
measure: measure.o scan.o $(CORE)
	$(CC) -o $@ $^ $(LDLIBS)
units_test: units_test.o $(CORE)
	$(CC) -o $@ $^ $(LDLIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c $<

tokenize.o: tokenize.h
folder.o: folder.h
index.o: index.h folder.h tokenize.h
query.o: query.h index.h topk.h
topk.o: topk.h
scan.o: scan.h folder.h topk.h query.h tokenize.h
main.o naive.o measure.o units_test.o: index.h query.h topk.h tokenize.h folder.h scan.h

test: units_test
	./units_test

clean:
	rm -f search naive measure units_test *.o

.PHONY: all test clean
