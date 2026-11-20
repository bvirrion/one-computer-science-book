// test-with: ../exercises/gheap.c
// The generic max-heap on doubles and on structures ordered by a field.
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef int (*compare)(const void *, const void *);
typedef struct { char *a; size_t n, cap, size; compare cmp; } gheap;
void gheap_init(gheap *h, size_t size, compare cmp);
void gheap_push(gheap *h, const void *x);
void gheap_pop(gheap *h, void *out);
void gheap_free(gheap *h);

typedef struct { char name[8]; int urgency; } patient;

static int by_double(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}
static int most_urgent(const void *a, const void *b) {  // urgency 1 first: reversed order
    return ((const patient *)b)->urgency - ((const patient *)a)->urgency;
}

int main(void) {
    gheap h;
    gheap_init(&h, sizeof(double), by_double);
    for (int i = 0; i < 1000; i++) {
        double x = (i * 7919) % 1000 / 10.0;
        gheap_push(&h, &x);
    }
    double prev = 1e9, x;
    while (h.n > 0) gheap_pop(&h, &x), assert(x <= prev), prev = x;
    gheap_free(&h);
    gheap_init(&h, sizeof(patient), most_urgent);
    patient ps[] = {{"Ana", 3}, {"Ben", 1}, {"Cleo", 4}, {"Dev", 2}}, p;
    for (int i = 0; i < 4; i++) gheap_push(&h, &ps[i]);
    gheap_pop(&h, &p);
    assert(strcmp(p.name, "Ben") == 0);
    gheap_pop(&h, &p);
    assert(strcmp(p.name, "Dev") == 0);
    gheap_free(&h);
    puts("gheap: ok");
    return 0;
}
