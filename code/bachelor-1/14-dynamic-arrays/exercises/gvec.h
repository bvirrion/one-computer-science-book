// gvec.h: a dynamic array of elements of any type, given by their size in bytes.
#ifndef GVEC_H
#define GVEC_H
#include <stddef.h>

typedef struct gvec gvec;

gvec *gvec_new(size_t elem_size);
void gvec_free(gvec *v);
size_t gvec_size(const gvec *v);
void *gvec_at(gvec *v, size_t i);           // address of element i; precondition: i < size
void gvec_push(gvec *v, const void *elem);  // copies elem_size bytes from elem
void gvec_pop(gvec *v, void *out);          // copies the last element to out, removes it
#endif
