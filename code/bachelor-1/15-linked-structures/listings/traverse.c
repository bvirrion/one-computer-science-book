// traverse.c: summing n ints in an array, in a list whose cells follow each other in
// memory, and in a list whose cells are scattered; nanoseconds per element, best of 5.
#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct cell {
    long value;
    struct cell *next;
} cell;

static double now(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static double time_list(const cell *head, long n, long *out) {
    double best = 1e9;
    for (int r = 0; r < 5; r++) {
        double t = now();
        long s = 0;
        for (const cell *p = head; p != NULL; p = p->next) s += p->value;
        best = (t = now() - t) < best ? t : best;
        *out = s;
    }
    return 1e9 * best / n;
}

int main(void) {
    long n = 1 << 22;
    long *array = malloc(n * sizeof *array);
    cell *cells = malloc(n * sizeof *cells);
    long *order = malloc(n * sizeof *order);
    for (long i = 0; i < n; i++) array[i] = i, cells[i].value = i, order[i] = i;
    for (long i = 0; i < n - 1; i++) cells[i].next = &cells[i + 1];  // in order
    cells[n - 1].next = NULL;
    double best = 1e9;
    long s = 0;
    for (int r = 0; r < 5; r++) {
        double t = now();
        s = 0;
        for (long i = 0; i < n; i++) s += array[i];
        best = (t = now() - t) < best ? t : best;
    }
    printf("array                %6.2f ns per element (sum %ld)\n", 1e9 * best / n, s);
    printf("list, cells in order %6.2f ns per element\n", time_list(cells, n, &s));
    srand(1);
    for (long i = n - 1; i > 0; i--) {  // shuffle the order of the cells
        long j = ((long)rand() * RAND_MAX + rand()) % (i + 1), k = order[i];
        order[i] = order[j], order[j] = k;
    }
    for (long i = 0; i < n - 1; i++) cells[order[i]].next = &cells[order[i + 1]];
    cells[order[n - 1]].next = NULL;
    printf("list, cells shuffled %6.2f ns per element\n", time_list(&cells[order[0]], n, &s));
    free(array), free(cells), free(order);
    return 0;
}
