// dlist_demo.c: a deque on a circular doubly linked list.
// capture: with=dlist.c
#include "dlist.h"
#include <stdio.h>

int main(void) {
    dlist l;
    dlist_init(&l);
    dlist_print(&l);
    dlist_push_back(&l, 2);
    dlist_push_back(&l, 3);
    dlist_push_front(&l, 1);
    dlist_print(&l);
    dnode *two = l.sentinel.next->next;
    dlist_insert_after(two, 20);
    dlist_remove(two);  // a known cell goes in constant time
    dlist_print(&l);
    int a = dlist_pop_back(&l);
    int b = dlist_pop_front(&l);
    printf("popped %d at the back and %d at the front\n", a, b);
    dlist_print(&l);
    dlist_clear(&l);
    return 0;
}
