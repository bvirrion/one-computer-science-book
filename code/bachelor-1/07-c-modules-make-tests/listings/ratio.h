// ratio.h: exact fractions. The interface: what a user of the module may rely on.
#ifndef RATIO_H
#define RATIO_H

struct ratio;                               // an opaque type: users never see its fields

// A new fraction num/den in lowest terms, with den > 0; NULL if den == 0 or out of memory.
// The caller owns the result and frees it with ratio_free.
struct ratio *ratio_new(long num, long den);
void ratio_free(struct ratio *r);
long ratio_num(const struct ratio *r);
long ratio_den(const struct ratio *r);
struct ratio *ratio_add(const struct ratio *a, const struct ratio *b);   // a new fraction
struct ratio *ratio_mul(const struct ratio *a, const struct ratio *b);   // a new fraction
int ratio_cmp(const struct ratio *a, const struct ratio *b);             // <0, 0 or >0

#endif
