// exo_free_bug.c: exercise 5, freeing a whole list.
// capture: cflags=-O0 -g -fsanitize=address exit
#include <stdlib.h>

typedef struct node {
    int value;
    struct node *next;
} node;

void free_all(node *head) {
    for (node *p = head; p != NULL; p = p->next) free(p);
}

int main(void) {
    node *head = NULL;
    for (int i = 0; i < 3; i++) {
        node *n = malloc(sizeof *n);
        *n = (node){i, head};
        head = n;
    }
    free_all(head);
    return 0;
}
