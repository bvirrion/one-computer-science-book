// region_of.c: guess the region a pointer points into, by the nearest marker.
// It relies on this machine's layout (regions far apart); the C standard
// promises nothing about comparing pointers into different objects.
#include <stdint.h>
#include <stdlib.h>
#include "region_of.h"

static int data_marker = 1;

static uintptr_t gap(uintptr_t a, uintptr_t b) { return a > b ? a - b : b - a; }

const char *region_of(const void *p, const void *stack_marker)
{
    void *heap_marker = malloc(1);
    uintptr_t a = (uintptr_t)p;
    uintptr_t marks[4] = {(uintptr_t)&region_of, (uintptr_t)&data_marker,
                          (uintptr_t)heap_marker, (uintptr_t)stack_marker};
    const char *names[4] = {"code", "static data", "heap", "stack"};
    int best = 0;
    for (int i = 1; i < 4; i++)
        if (gap(a, marks[i]) < gap(a, marks[best]))
            best = i;
    free(heap_marker);
    return names[best];
}
