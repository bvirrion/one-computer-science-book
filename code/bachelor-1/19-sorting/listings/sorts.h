// sorts.h: comparison sorts of int arrays, each counting its key comparisons.
#ifndef SORTS_H
#define SORTS_H

extern long sort_compares;

void insertion_sort(int *a, int n);
void quicksort_basic(int *a, int n);  // Lomuto, last element as pivot
void quicksort(int *a, int n);        // median of three, small side first, insertion sort below 16
void quicksort3(int *a, int n);       // three-way partition: <, ==, >
void merge_sort(int *a, int n);       // top-down
void merge_sort_bottom_up(int *a, int n);
void heap_sort(int *a, int n);
#endif
