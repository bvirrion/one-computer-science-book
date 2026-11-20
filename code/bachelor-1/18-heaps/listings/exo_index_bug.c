// exo_index_bug.c: exercise 6, index formulas from a book that numbers from 1.
#include <stdio.h>

int parent(int i) { return i / 2; }
int left(int i) { return 2 * i; }

int main(void) {
    int a[] = {1, 3, 2, 7, 4};  // a min-heap, indices from 0
    for (int i = 0; i < 5; i++)
        printf("a[%d] = %d: parent a[%d] = %d, left child a[%d]\n", i, a[i], parent(i),
               a[parent(i)], left(i));
    return 0;
}
