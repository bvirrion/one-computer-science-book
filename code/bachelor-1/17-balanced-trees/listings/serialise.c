// serialise.c: a search tree written to a file in preorder with "#" for empty subtrees,
// then read back.
// capture: with=bst.c
#include "bst.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void write_tree(const node *t, FILE *f) {
    if (t == NULL) {
        fputs("# ", f);
        return;
    }
    fprintf(f, "%s %d ", t->key, t->value);
    write_tree(t->left, f);
    write_tree(t->right, f);
}

static char store[100][32];  // the keys read back live here
static int stored;

static node *read_tree(FILE *f) {
    char word[32];
    if (fscanf(f, "%31s", word) != 1 || strcmp(word, "#") == 0) return NULL;
    node *t = malloc(sizeof *t);
    if (t == NULL || stored == 100 || fscanf(f, "%d", &t->value) != 1) exit(1);
    t->key = strcpy(store[stored++], word);
    t->left = read_tree(f);  // the same order as the writing
    t->right = read_tree(f);
    return t;
}

int main(void) {
    const char *names[] = {"Mia", "Eli", "Tom", "Bea", "Ivy", "Pia", "Zoe"};
    node *t = NULL;
    for (int i = 0; i < 7; i++) t = bst_put(t, names[i], i);
    FILE *f = tmpfile();
    if (f == NULL) return 1;
    write_tree(t, f);
    rewind(f);
    char text[200];
    if (fgets(text, sizeof text, f) == NULL) return 1;
    text[strcspn(text, "\n")] = '\0';
    if (strlen(text) > 0) text[strlen(text) - 1] = '\0';  // the last space
    printf("file: %s\n", text);
    rewind(f);
    node *copy = read_tree(f);
    fclose(f);
    printf("read back: height %d, size %d\n", bst_height(copy), bst_size(copy));
    bst_show(copy);
    bst_free(t), bst_free(copy);
    return 0;
}
