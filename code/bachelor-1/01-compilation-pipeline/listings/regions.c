// regions.c: where the objects of a running program live, in address order.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int initialised_global = 42;   // static data, initialised
int zero_global;               // static data, zero-initialised
static int helper(int x) { return x + 1; }

struct place { const char *name; uintptr_t addr; };
static int by_addr(const void *a, const void *b)
{
    uintptr_t x = ((const struct place *)a)->addr;
    uintptr_t y = ((const struct place *)b)->addr;
    return (x > y) - (x < y);
}

int main(void)
{
    int local = helper(1);                    // the call stack
    int *block = malloc(sizeof *block);       // the heap
    if (block == NULL) return 1;              // no memory
    const char *literal = "a string literal"; // read-only data
    struct place p[] = {
        {"local variable (stack)", (uintptr_t)&local},
        {"heap block (malloc)", (uintptr_t)block},
        {"zero-initialised global", (uintptr_t)&zero_global},
        {"initialised global", (uintptr_t)&initialised_global},
        {"string literal", (uintptr_t)literal},
        {"function code", (uintptr_t)&helper},
    };
    size_t n = sizeof p / sizeof p[0];
    qsort(p, n, sizeof p[0], by_addr);
    puts("from low addresses to high addresses:");
    for (size_t i = 0; i < n; i++)
        printf("  %zu. %s\n", i + 1, p[i].name);
    printf("the stack lies %s the heap\n",
           (uintptr_t)&local > (uintptr_t)block ? "above" : "below");
    free(block);
    return 0;
}
