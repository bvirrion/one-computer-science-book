// dlist.h: circular doubly linked lists of int with a sentinel; also a deque.
#ifndef DLIST_H
#define DLIST_H
#include <stdbool.h>

typedef struct dnode {
    int value;
    struct dnode *prev, *next;
} dnode;

typedef struct {
    dnode sentinel;  // sentinel.next is the first cell, sentinel.prev the last
} dlist;

void dlist_init(dlist *l);                     // the empty list
bool dlist_empty(const dlist *l);
dnode *dlist_insert_after(dnode *cell, int x);  // cell may be the sentinel
void dlist_remove(dnode *cell);                 // cell must not be the sentinel
void dlist_push_front(dlist *l, int x);
void dlist_push_back(dlist *l, int x);
int dlist_pop_front(dlist *l);                  // precondition: not empty
int dlist_pop_back(dlist *l);                   // precondition: not empty
void dlist_print(const dlist *l);
void dlist_clear(dlist *l);
#endif
