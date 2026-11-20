// test-with: ../exercises/gvec.c
// The generic array with doubles and with a struct.
#include "../exercises/gvec.h"
#include <assert.h>
#include <stdio.h>

typedef struct {
    char name[8];
    int year;
} book;

int main(void) {
    gvec *d = gvec_new(sizeof(double));
    for (int i = 0; i < 5000; i++) {
        double x = i / 4.0;
        gvec_push(d, &x);
    }
    assert(gvec_size(d) == 5000 && *(double *)gvec_at(d, 4000) == 1000.0);
    for (int i = 4999; i >= 0; i--) {
        double x;
        gvec_pop(d, &x);
        assert(x == i / 4.0);
    }
    gvec_free(d);
    gvec *b = gvec_new(sizeof(book));
    book in[3] = {{"Dune", 1965}, {"Emma", 1815}, {"Ubik", 1969}};
    for (int i = 0; i < 3; i++) gvec_push(b, &in[i]);
    ((book *)gvec_at(b, 1))->year++;
    book out;
    gvec_pop(b, &out);
    assert(out.year == 1969 && ((book *)gvec_at(b, 1))->year == 1816);
    gvec_free(b);
    puts("gvec: ok");
    return 0;
}
