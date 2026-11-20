// Exercise 9: the allocation of short_alloc.c with the multiplication checked
// before it is done, in the type the size is computed in.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { uint32_t book, reader; } loan;

loan *alloc_loans(uint32_t count) {
    if (count > UINT32_MAX / sizeof(loan)) return NULL;  // count * 8 would wrap
    return malloc((size_t)count * sizeof(loan));
}

int main(void) {
    uint32_t counts[] = {3, 1000000, (1u << 29) + 1};
    for (int i = 0; i < 3; i++) {
        loan *p = alloc_loans(counts[i]);
        printf("count %u: %s\n", counts[i], p ? "allocated" : "refused");
        free(p);
    }
    return 0;
}
