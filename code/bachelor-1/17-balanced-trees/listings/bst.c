// bst.c: every operation follows one path from the root.
#include "bst.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

node *bst_put(node *t, const char *key, int value) {
    if (t == NULL) {
        node *n = malloc(sizeof *n);
        if (n == NULL) exit(1);
        *n = (node){key, value, NULL, NULL};
        return n;
    }
    int c = strcmp(key, t->key);
    if (c < 0) t->left = bst_put(t->left, key, value);
    else if (c > 0) t->right = bst_put(t->right, key, value);
    else t->value = value;
    return t;
}

bool bst_get(const node *t, const char *key, int *value) {
    while (t != NULL) {
        int c = strcmp(key, t->key);
        if (c == 0) {
            *value = t->value;
            return true;
        }
        t = c < 0 ? t->left : t->right;
    }
    return false;
}

const node *bst_min(const node *t) {
    while (t != NULL && t->left != NULL) t = t->left;
    return t;
}

const char *bst_floor(const node *t, const char *key) {
    const char *best = NULL;
    while (t != NULL) {
        int c = strcmp(key, t->key);
        if (c == 0) return t->key;
        if (c < 0) t = t->left;
        else best = t->key, t = t->right;  // a candidate; a larger one may be on the right
    }
    return best;
}

const char *bst_next(const node *t, const char *key) {
    const char *best = NULL;
    while (t != NULL)
        if (strcmp(key, t->key) < 0) best = t->key, t = t->left;
        else t = t->right;
    return best;
}

node *bst_delete(node *t, const char *key) {
    if (t == NULL) return NULL;
    int c = strcmp(key, t->key);
    if (c < 0) t->left = bst_delete(t->left, key);
    else if (c > 0) t->right = bst_delete(t->right, key);
    else if (t->left == NULL || t->right == NULL) {  // zero or one child: splice it out
        node *child = t->left != NULL ? t->left : t->right;
        free(t);
        return child;
    } else {  // two children: take the successor's key, then delete the successor
        const node *s = bst_min(t->right);
        t->key = s->key, t->value = s->value;
        t->right = bst_delete(t->right, s->key);
    }
    return t;
}

int bst_height(const node *t) {
    if (t == NULL) return -1;
    int l = bst_height(t->left), r = bst_height(t->right);
    return 1 + (l > r ? l : r);
}

int bst_size(const node *t) { return t == NULL ? 0 : 1 + bst_size(t->left) + bst_size(t->right); }

void bst_inorder(const node *t, void (*visit)(const node *)) {
    if (t == NULL) return;
    bst_inorder(t->left, visit);
    visit(t);
    bst_inorder(t->right, visit);
}

static void show(const node *t, int depth) {
    if (t == NULL) return;
    show(t->right, depth + 1);
    printf("%*s%s\n", 4 * depth, "", t->key);
    show(t->left, depth + 1);
}

void bst_show(const node *t) { show(t, 0); }

void bst_free(node *t) {
    if (t == NULL) return;
    bst_free(t->left);
    bst_free(t->right);
    free(t);
}
