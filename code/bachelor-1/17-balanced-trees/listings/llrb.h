// llrb.h: a left-leaning red-black tree (insertion only).
#ifndef LLRB_H
#define LLRB_H
#include <stdbool.h>

typedef struct rb {
    const char *key;
    int value;
    bool red;  // the colour of the link from the parent
    struct rb *left, *right;
} rb;

rb *llrb_put(rb *t, const char *key, int value);  // returns the new root, which is black
bool llrb_get(const rb *t, const char *key, int *value);
int llrb_height(const rb *t);
int llrb_black_height(const rb *t);  // black links on the leftmost path
bool llrb_check(const rb *t);        // order, no red right link, no two reds in a row, equal black heights
void llrb_show(const rb *t);         // red nodes marked with *
void llrb_free(rb *t);
#endif
