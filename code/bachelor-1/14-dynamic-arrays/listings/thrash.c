// thrash.c: two shrinking policies on a sequence that hovers at a power of 2.
#include <stdio.h>

typedef struct {
    long size, capacity, copies, shrink_divisor;  // shrink when size <= capacity / d
} array;

static void push(array *a) {
    if (a->size == a->capacity) {
        a->copies += a->size;
        a->capacity *= 2;
    }
    a->size++;
}

static void pop(array *a) {
    a->size--;
    if (a->capacity > 1 && a->size <= a->capacity / a->shrink_divisor) {
        a->copies += a->size;
        a->capacity /= 2;
    }
}

int main(void) {
    for (long d = 2; d <= 4; d += 2) {
        array a = {0, 1, 0, d};
        for (long i = 0; i < 1024; i++) push(&a);  // fill to a power of 2
        long before = a.copies, m = 1000;
        for (long i = 0; i < m; i++) i % 2 == 0 ? push(&a) : pop(&a);
        printf("shrink at 1/%ld: %ld operations after the fill, %ld copies, %.1f each\n",
               d, m, a.copies - before, (double)(a.copies - before) / m);
    }
    return 0;
}
