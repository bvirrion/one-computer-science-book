// capture: cflags=-O0 -g -fsanitize=address exit
// short_alloc.c -- a loan file announces how many records follow; the reader
// allocates count * 8 bytes, computed in 32 bits. A count of 2^29 + 1 wraps around
// to 8 bytes, and the second record is written past the end of the allocation.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { uint32_t book, reader; } loan;  // 8 bytes

int main(void) {
    setvbuf(stdout, NULL, _IOLBF, 0);
    uint32_t count = (1u << 29) + 1;           // read from the file in a real program
    uint32_t bytes = count * sizeof(loan);     // 2^32 + 8 wraps around to 8
    printf("count %u, bytes %u\n", count, bytes);
    loan *loans = malloc(bytes);
    if (!loans) return 1;
    for (uint32_t i = 0; i < count; i++) {     // the loop trusts count, not bytes
        loans[i].book = i;
        loans[i].reader = 7;
    }
    free(loans);
    return 0;
}
