// iter.c: one loop over a list and over an array, through an iterator; and a callback.
// capture: with=list.c
#include "list.h"
#include <stdbool.h>
#include <stdio.h>

typedef struct {            // an iterator: where we are, and how to move on
    const node *cell;       // for a list
    const int *at, *end;    // for an array
} iter;

static iter list_begin(const node *head) { return (iter){head, NULL, NULL}; }
static iter array_begin(const int *a, size_t n) { return (iter){NULL, a, a + n}; }

static bool has_next(const iter *it) { return it->cell != NULL || it->at != it->end; }

static int next(iter *it) {
    if (it->cell != NULL) {
        int x = it->cell->value;
        it->cell = it->cell->next;
        return x;
    }
    return *it->at++;
}

static long sum(iter it) {  // knows nothing of lists or arrays
    long s = 0;
    while (has_next(&it)) s += next(&it);
    return s;
}

static void list_each(const node *head, void (*f)(int)) {  // the callback style
    for (const node *p = head; p != NULL; p = p->next) f(p->value);
}

static void show(int x) { printf("<%d>", x); }

int main(void) {
    node *head = NULL;
    for (int x = 4; x >= 1; x--) list_push(&head, x);
    int a[] = {10, 20, 30};
    printf("sum of the list %ld, of the array %ld\n", sum(list_begin(head)),
           sum(array_begin(a, 3)));
    list_each(head, show);
    printf("\n");
    list_free(head);
    return 0;
}
