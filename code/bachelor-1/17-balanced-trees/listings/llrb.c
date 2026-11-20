// llrb.c: three local repairs on the way back up keep the tree black-balanced.
#include "llrb.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool is_red(const rb *t) { return t != NULL && t->red; }

static rb *rotate_left(rb *h) {  // a red right link becomes a red left link
    rb *x = h->right;
    h->right = x->left;
    x->left = h;
    x->red = h->red;
    h->red = true;
    return x;
}

static rb *rotate_right(rb *h) {
    rb *x = h->left;
    h->left = x->right;
    x->right = h;
    x->red = h->red;
    h->red = true;
    return x;
}

static void flip(rb *h) {  // split a temporary 4-node: the middle key goes up
    h->red = true;
    h->left->red = h->right->red = false;
}

static rb *put(rb *h, const char *key, int value) {
    if (h == NULL) {
        rb *n = malloc(sizeof *n);
        if (n == NULL) exit(1);
        *n = (rb){key, value, true, NULL, NULL};  // a new key joins its parent's node
        return n;
    }
    int c = strcmp(key, h->key);
    if (c < 0) h->left = put(h->left, key, value);
    else if (c > 0) h->right = put(h->right, key, value);
    else h->value = value;
    if (is_red(h->right) && !is_red(h->left)) h = rotate_left(h);
    if (is_red(h->left) && is_red(h->left->left)) h = rotate_right(h);
    if (is_red(h->left) && is_red(h->right)) flip(h);
    return h;
}

rb *llrb_put(rb *t, const char *key, int value) {
    t = put(t, key, value);
    t->red = false;
    return t;
}

bool llrb_get(const rb *t, const char *key, int *value) {
    while (t != NULL) {
        int c = strcmp(key, t->key);
        if (c == 0) return *value = t->value, true;
        t = c < 0 ? t->left : t->right;
    }
    return false;
}

int llrb_height(const rb *t) {
    if (t == NULL) return -1;
    int l = llrb_height(t->left), r = llrb_height(t->right);
    return 1 + (l > r ? l : r);
}

int llrb_black_height(const rb *t) {
    int b = 0;
    for (; t != NULL; t = t->left) b += !t->red;
    return b;
}

static int check(const rb *t, const char *lo, const char *hi) {  // black height, or -1
    if (t == NULL) return 0;
    if ((lo != NULL && strcmp(t->key, lo) <= 0) || (hi != NULL && strcmp(t->key, hi) >= 0)) return -1;
    if (is_red(t->right) || (t->red && is_red(t->left))) return -1;
    int l = check(t->left, lo, t->key), r = check(t->right, t->key, hi);
    if (l < 0 || l != r) return -1;
    return l + !t->red;
}

bool llrb_check(const rb *t) { return !is_red(t) && check(t, NULL, NULL) >= 0; }

static void show(const rb *t, int depth) {
    if (t == NULL) return;
    show(t->right, depth + 1);
    printf("%*s%s%s\n", 4 * depth, "", t->red ? "*" : "", t->key);
    show(t->left, depth + 1);
}

void llrb_show(const rb *t) { show(t, 0); }

void llrb_free(rb *t) {
    if (t == NULL) return;
    llrb_free(t->left);
    llrb_free(t->right);
    free(t);
}
