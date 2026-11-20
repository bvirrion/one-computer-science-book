/* heap.h -- a heap of cells for the collectors. A reference is a cell's index, or NIL. */
#ifndef HEAP_H
#define HEAP_H

#define NIL (-1)
#define MAX_CELLS 100000
#define MAX_ROOTS 4096

struct cell {
    int meta;    /* the collector's: a mark bit, or a forwarding pointer */
    int data;    /* an integer the program stores */
    int ref[2];  /* two references */
};

/* The roots: the references the program holds outside the heap (its variables). */
extern int roots[MAX_ROOTS];
extern int nroots;

struct gc_stats {
    long allocated, collections, visited, swept;  /* visited: marked or copied cells */
};
extern struct gc_stats gc_stats;

void gc_init(int cells);                 /* a heap of `cells` cells, all free */
int gc_alloc(int data, int r0, int r1);  /* NIL when the heap is full of live cells */
struct cell *gc_cell(int c);             /* valid until the next gc_alloc */
#endif
