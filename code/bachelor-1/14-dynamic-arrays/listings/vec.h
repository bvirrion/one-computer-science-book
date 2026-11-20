// vec.h: the interface of the abstract type "dynamic array of int".
#ifndef VEC_H
#define VEC_H
#include <stddef.h>

typedef struct vec vec;               // opaque: the fields stay in the implementation

vec *vec_new(void);                   // constructor: an empty array
void vec_free(vec *v);
size_t vec_size(const vec *v);        // accessors
int vec_get(const vec *v, size_t i);  // precondition: i < size
void vec_set(vec *v, size_t i, int x);  // transformers; precondition: i < size
void vec_push(vec *v, int x);         // add x at the end
int vec_pop(vec *v);                  // remove and return the last; precondition: size > 0
size_t vec_capacity(const vec *v);    // for the experiments: cells reserved
long vec_copies(const vec *v);        // for the experiments: elements copied so far
#endif
