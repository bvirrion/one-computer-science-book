// dlist.c: with a sentinel, insertion and removal have no special case.
#include "dlist.h"
#include <stdio.h>
#include <stdlib.h>

void dlist_init(dlist *l) {
    l->sentinel.next = l->sentinel.prev = &l->sentinel;  // the sentinel alone
}

bool dlist_empty(const dlist *l) { return l->sentinel.next == &l->sentinel; }

dnode *dlist_insert_after(dnode *cell, int x) {
    dnode *n = malloc(sizeof *n);
    if (n == NULL) {
        perror("dlist");
        exit(1);
    }
    *n = (dnode){x, cell, cell->next};
    cell->next->prev = n;  // the old neighbour now points back to n
    cell->next = n;
    return n;
}

void dlist_remove(dnode *cell) {
    cell->prev->next = cell->next;  // both neighbours always exist
    cell->next->prev = cell->prev;
    free(cell);
}

void dlist_push_front(dlist *l, int x) { dlist_insert_after(&l->sentinel, x); }
void dlist_push_back(dlist *l, int x) { dlist_insert_after(l->sentinel.prev, x); }

int dlist_pop_front(dlist *l) {
    int x = l->sentinel.next->value;
    dlist_remove(l->sentinel.next);
    return x;
}

int dlist_pop_back(dlist *l) {
    int x = l->sentinel.prev->value;
    dlist_remove(l->sentinel.prev);
    return x;
}

void dlist_print(const dlist *l) {
    printf("[S]");
    for (const dnode *p = l->sentinel.next; p != &l->sentinel; p = p->next)
        printf(" <-> %d", p->value);
    printf(" <-> [S]\n");
}

void dlist_clear(dlist *l) {
    while (!dlist_empty(l)) dlist_pop_front(l);
}
