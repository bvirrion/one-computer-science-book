// intvec.h: a growable array of int, written by hand.
#ifndef INTVEC_H
#define INTVEC_H
#include <stddef.h>

struct intvec {
    int *data;          // a heap block of cap ints, of which the first len are used
    size_t len;
    size_t cap;
    long copies;        // elements copied by the growths so far
};

void intvec_init(struct intvec *v);             // an empty vector, no block yet
int intvec_push(struct intvec *v, int x);       // appends x; 0, or -1 if out of memory
void intvec_free(struct intvec *v);             // frees the block; v is empty again

#endif
