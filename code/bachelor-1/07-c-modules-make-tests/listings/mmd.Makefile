# mmd.Makefile: pattern rules, and header dependencies written by the compiler.
CC = gcc
CFLAGS = -std=c17 -O2 -Wall -Wextra -Werror -MMD -MP
SRC = loans_main.c loans.c csv.c date.c
OBJ = $(SRC:.c=.o)

checker: $(OBJ)
	$(CC) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f checker $(OBJ) $(OBJ:.o=.d)

.PHONY: clean
-include $(OBJ:.o=.d)
