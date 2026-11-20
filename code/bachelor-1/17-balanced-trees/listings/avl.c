// avl.c: insertion as in a search tree, then rotations on the way back up.
#include "avl.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long avl_single, avl_double;

int avl_height(const avl *t) { return t == NULL ? -1 : t->height; }

static void update(avl *t) {
    int l = avl_height(t->left), r = avl_height(t->right);
    t->height = 1 + (l > r ? l : r);
}

static int balance(const avl *t) { return avl_height(t->right) - avl_height(t->left); }

static avl *rotate_right(avl *y) {  // the left child x becomes the root of the subtree
    avl *x = y->left;
    y->left = x->right;  // the middle subtree changes parent
    x->right = y;
    update(y);
    update(x);
    return x;
}

static avl *rotate_left(avl *x) {
    avl *y = x->right;
    x->right = y->left;
    y->left = x;
    update(x);
    update(y);
    return y;
}

static avl *rebalance(avl *t) {
    update(t);
    if (balance(t) == -2) {  // left-heavy
        if (balance(t->left) > 0) t->left = rotate_left(t->left), avl_double++;  // case LR
        else avl_single++;                                                       // case LL
        return rotate_right(t);
    }
    if (balance(t) == 2) {  // right-heavy: the mirror image
        if (balance(t->right) < 0) t->right = rotate_right(t->right), avl_double++;  // RL
        else avl_single++;                                                          // RR
        return rotate_left(t);
    }
    return t;
}

avl *avl_put(avl *t, const char *key, int value) {
    if (t == NULL) {
        avl *n = malloc(sizeof *n);
        if (n == NULL) exit(1);
        *n = (avl){key, value, 0, NULL, NULL};
        return n;
    }
    int c = strcmp(key, t->key);
    if (c < 0) t->left = avl_put(t->left, key, value);
    else if (c > 0) t->right = avl_put(t->right, key, value);
    else t->value = value;
    return rebalance(t);
}

bool avl_get(const avl *t, const char *key, int *value) {
    while (t != NULL) {
        int c = strcmp(key, t->key);
        if (c == 0) return *value = t->value, true;
        t = c < 0 ? t->left : t->right;
    }
    return false;
}

static bool check(const avl *t, const char *lo, const char *hi) {  // keys strictly in (lo, hi)
    if (t == NULL) return true;
    if ((lo != NULL && strcmp(t->key, lo) <= 0) || (hi != NULL && strcmp(t->key, hi) >= 0))
        return false;
    int l = avl_height(t->left), r = avl_height(t->right);
    return t->height == 1 + (l > r ? l : r) && abs(r - l) <= 1 && check(t->left, lo, t->key) &&
           check(t->right, t->key, hi);
}

bool avl_check(const avl *t) { return check(t, NULL, NULL); }

static void show(const avl *t, int depth) {
    if (t == NULL) return;
    show(t->right, depth + 1);
    printf("%*s%s (%+d)\n", 4 * depth, "", t->key, balance(t));
    show(t->left, depth + 1);
}

void avl_show(const avl *t) { show(t, 0); }

void avl_free(avl *t) {
    if (t == NULL) return;
    avl_free(t->left);
    avl_free(t->right);
    free(t);
}
