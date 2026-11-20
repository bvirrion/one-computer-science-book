// exo_chain.c: freeing a chain of three nodes.
#include <stdio.h>
#include <stdlib.h>

struct node {
    int value;
    struct node *next;
};

int main(void)
{
    struct node *head = NULL;
    for (int v = 3; v >= 1; v--) {                     // builds 1 -> 2 -> 3
        struct node *n = malloc(sizeof *n);
        if (n == NULL)
            return 1;
        n->value = v;
        n->next = head;
        head = n;
    }
    for (struct node *p = head; p != NULL; p = p->next)
        free(p);
    printf("freed\n");
    return 0;
}
