// test-with: ../listings/dlist.c ../exercises/deque_ring.c
// The sentinel list as a deque, and the ring deque, against a plain array model.
#include "dlist.h"
#include <assert.h>
#include <stdio.h>

typedef struct { int data[8]; size_t head, count; } deque;  // as in deque_ring.c
void deque_init(deque *d);
void deque_push_back(deque *d, int x);
void deque_push_front(deque *d, int x);
int deque_pop_front(deque *d);
int deque_pop_back(deque *d);

int main(void) {
    dlist l;
    dlist_init(&l);
    deque d;
    deque_init(&d);
    int model[200], lo = 100, hi = 100;  // the deque is model[lo..hi)
    unsigned state = 3;
    for (int i = 0; i < 5000; i++) {
        state = state * 1103515245u + 12345u;
        int op = (state >> 16) % 4, size = hi - lo;
        if (size == 0 || (op < 2 && size < 8)) {
            if (op % 2 == 0) dlist_push_back(&l, i), deque_push_back(&d, i), model[hi++] = i;
            else dlist_push_front(&l, i), deque_push_front(&d, i), model[--lo] = i;
        } else if (op % 2 == 0) {
            int x = model[--hi];
            assert(dlist_pop_back(&l) == x && deque_pop_back(&d) == x);
        } else {
            int x = model[lo++];
            assert(dlist_pop_front(&l) == x && deque_pop_front(&d) == x);
        }
        if (lo < 20 || hi > 180) {  // recentre the model
            int n = hi - lo;
            for (int j = 0; j < n; j++) model[100 + j] = model[lo + j];
            lo = 100, hi = 100 + n;
        }
        assert(dlist_empty(&l) == (lo == hi));
        assert(l.sentinel.next->prev == &l.sentinel && l.sentinel.prev->next == &l.sentinel);
    }
    dlist_clear(&l);
    assert(dlist_empty(&l));
    puts("dlist and ring deque: ok");
    return 0;
}
