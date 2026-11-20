# stale.Makefile: one rule is missing a prerequisite.
limits: limits_main.o
	gcc -o limits limits_main.o

limits_main.o: limits_main.c
	gcc -std=c17 -O2 -c limits_main.c
