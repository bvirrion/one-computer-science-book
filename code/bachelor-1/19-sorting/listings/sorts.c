// sorts.c: quicksort in three versions, merge sort in two, insertion sort and heapsort.
#include "sorts.h"
#include <stdlib.h>
#include <string.h>

long sort_compares;

static int less(int x, int y) { return sort_compares++, x < y; }
static void swap(int *a, int i, int j) { int t = a[i]; a[i] = a[j], a[j] = t; }

void insertion_sort(int *a, int n) {
    for (int i = 1; i < n; i++)
        for (int j = i; j > 0 && less(a[j], a[j - 1]); j--) swap(a, j, j - 1);
}

static int partition(int *a, int lo, int hi) {  // a[lo..hi), pivot a[hi - 1]; as in chapter 12
    int p = a[hi - 1], k = lo;
    for (int j = lo; j < hi - 1; j++)
        if (less(a[j], p)) swap(a, k++, j);  // invariant: a[lo..k) < p <= a[k..j)
    swap(a, k, hi - 1);
    return k;
}

static void qs_basic(int *a, int lo, int hi) {
    if (hi - lo < 2) return;
    int k = partition(a, lo, hi);  // a[lo..k) < a[k] <= a(k..hi)
    qs_basic(a, lo, k);
    qs_basic(a, k + 1, hi);
}

void quicksort_basic(int *a, int n) { qs_basic(a, 0, n); }

static void qs(int *a, int lo, int hi) {
    while (hi - lo > 16) {
        int mid = lo + (hi - lo) / 2;  // median of three to the pivot position hi - 1
        if (less(a[mid], a[lo])) swap(a, mid, lo);
        if (less(a[hi - 1], a[lo])) swap(a, hi - 1, lo);
        if (less(a[mid], a[hi - 1])) swap(a, mid, hi - 1);
        int k = partition(a, lo, hi);
        if (k - lo < hi - k) qs(a, lo, k), lo = k + 1;  // recurse on the smaller side,
        else qs(a, k + 1, hi), hi = k;                  // loop on the larger one
    }
    insertion_sort(a + lo, hi - lo);  // small parts
}

void quicksort(int *a, int n) { qs(a, 0, n); }

static void qs3(int *a, int lo, int hi) {
    if (hi - lo < 2) return;
    int p = a[lo + (hi - lo) / 2], lt = lo, i = lo, gt = hi;
    while (i < gt)  // invariant: a[lo..lt) < p, a[lt..i) == p, a[gt..hi) > p
        if (less(a[i], p)) swap(a, lt++, i++);
        else if (less(p, a[i])) swap(a, i, --gt);
        else i++;
    qs3(a, lo, lt);
    qs3(a, gt, hi);
}

void quicksort3(int *a, int n) { qs3(a, 0, n); }

static void merge(int *a, int lo, int mid, int hi, int *tmp) {  // a[lo..mid), a[mid..hi) sorted
    memcpy(tmp + lo, a + lo, (size_t)(hi - lo) * sizeof *a);
    int i = lo, j = mid;
    for (int k = lo; k < hi; k++)
        if (i < mid && (j == hi || !less(tmp[j], tmp[i]))) a[k] = tmp[i++];  // ties: left first
        else a[k] = tmp[j++];
}

static void ms(int *a, int lo, int hi, int *tmp) {
    if (hi - lo < 2) return;
    int mid = lo + (hi - lo) / 2;
    ms(a, lo, mid, tmp);
    ms(a, mid, hi, tmp);
    merge(a, lo, mid, hi, tmp);
}

void merge_sort(int *a, int n) {
    int *tmp = malloc((size_t)n * sizeof *tmp + 1);
    if (tmp == NULL) exit(1);
    ms(a, 0, n, tmp);
    free(tmp);
}

void merge_sort_bottom_up(int *a, int n) {  // runs of width 1, 2, 4, ... merged in pairs
    int *tmp = malloc((size_t)n * sizeof *tmp + 1);
    if (tmp == NULL) exit(1);
    for (int w = 1; w < n; w *= 2)
        for (int lo = 0; lo + w < n; lo += 2 * w)
            merge(a, lo, lo + w, lo + 2 * w < n ? lo + 2 * w : n, tmp);
    free(tmp);
}

static void sift(int *a, int n, int i) {
    for (int c; (c = 2 * i + 1) < n; i = c) {
        if (c + 1 < n && less(a[c], a[c + 1])) c++;
        if (!less(a[i], a[c])) return;
        swap(a, i, c);
    }
}

void heap_sort(int *a, int n) {
    for (int i = n / 2 - 1; i >= 0; i--) sift(a, n, i);
    for (int end = n - 1; end > 0; end--) swap(a, 0, end), sift(a, end, 0);
}
