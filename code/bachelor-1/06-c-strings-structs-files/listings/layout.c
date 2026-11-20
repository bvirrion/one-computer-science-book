// layout.c: the same fields in two orders.
#include <stddef.h>
#include <stdio.h>

struct loose {
    char station;
    double temp;
    char flag;
    int date;
};

struct tight {
    double temp;
    int date;
    char station;
    char flag;
};

int main(void)
{
    printf("alignments: char %zu, int %zu, double %zu\n",
           _Alignof(char), _Alignof(int), _Alignof(double));
    printf("loose: size %2zu  station@%zu temp@%zu flag@%zu date@%zu\n", sizeof(struct loose),
           offsetof(struct loose, station), offsetof(struct loose, temp),
           offsetof(struct loose, flag), offsetof(struct loose, date));
    printf("tight: size %2zu  temp@%zu date@%zu station@%zu flag@%zu\n", sizeof(struct tight),
           offsetof(struct tight, temp), offsetof(struct tight, date),
           offsetof(struct tight, station), offsetof(struct tight, flag));
    struct tight a[3];
    printf("array of 3 tight: %zu bytes, a[1] starts %td bytes after a[0]\n",
           sizeof a, (char *)&a[1] - (char *)&a[0]);
    return 0;
}
