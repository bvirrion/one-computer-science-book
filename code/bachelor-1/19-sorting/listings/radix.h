// radix.h: counting sort by one decimal digit, and LSD radix sort built on it.
#ifndef RADIX_H
#define RADIX_H

void counting_sort_digit(const int *in, int *out, int n, int place);  // stable; place = 1, 10, ...
void radix_sort(int *a, int n, int digits);  // non-negative keys of at most `digits` digits
#endif
