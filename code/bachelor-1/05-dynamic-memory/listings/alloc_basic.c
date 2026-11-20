// alloc_basic.c: an array whose length is known only when the program runs.
#include <stdio.h>
// capture: args=1000
#include <stdlib.h>

int main(int argc, char **argv)
{
    size_t n = argc > 1 ? (size_t)atoi(argv[1]) : 10;
    int *squares = malloc(n * sizeof *squares);      // room for n ints, on the heap
    if (squares == NULL) {
        printf("out of memory\n");
        return 1;
    }
    for (size_t i = 0; i < n; i++)
        squares[i] = (int)(i * i);
    long sum = 0;
    for (size_t i = 0; i < n; i++)
        sum += squares[i];
    printf("%zu squares, sum %ld, last %d\n", n, sum, squares[n - 1]);
    free(squares);                                   // give the block back
    int *zeros = calloc(n, sizeof *zeros);           // calloc: the block starts at zero
    if (zeros == NULL)
        return 1;
    printf("calloc gave %d %d %d ...\n", zeros[0], zeros[1], zeros[2]);
    free(zeros);
    return 0;
}
