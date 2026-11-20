// exo_delete_bug.c: exercise 5, linear probing with a deletion that frees the slot.
#include <stdio.h>

enum { M = 7, EMPTY = -1 };
int slot[M] = {EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY};

void put(int key) {
    int i = key % M;
    while (slot[i] != EMPTY) i = (i + 1) % M;
    slot[i] = key;
}

int find(int key) {  // the slot of key, or -1
    for (int i = key % M; slot[i] != EMPTY; i = (i + 1) % M)
        if (slot[i] == key) return i;
    return -1;
}

void delete(int key) {
    int i = find(key);
    if (i >= 0) slot[i] = EMPTY;
}

int main(void) {
    put(10), put(17), put(24), put(5);  // 10, 17 and 24 all hash to 3
    delete(17);
    printf("find(24) = %d, find(5) = %d, find(10) = %d\n", find(24), find(5), find(10));
    return 0;
}
