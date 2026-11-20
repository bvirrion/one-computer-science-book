// remove_pp.c: removing a cell, with a special case for the head or with a pointer to a link.
// capture: with=list.c
#include "list.h"
#include <stdlib.h>

int remove_cases(node **head, int x) {
    if (*head == NULL) return 0;
    if ((*head)->value == x) {  // special case: the first cell
        node *dead = *head;
        *head = dead->next;
        free(dead);
        return 1;
    }
    node *prev = *head;  // general case: find the cell before
    while (prev->next != NULL && prev->next->value != x) prev = prev->next;
    if (prev->next == NULL) return 0;
    node *dead = prev->next;
    prev->next = dead->next;
    free(dead);
    return 1;
}

int main(void) {
    node *a = NULL, *b = NULL;
    for (int x = 4; x >= 1; x--) list_push(&a, x), list_push(&b, x);
    for (int x = 1; x <= 5; x += 2) remove_cases(&a, x), list_remove(&b, x);
    list_print(a);
    list_print(b);
    list_free(a);
    list_free(b);
    return 0;
}
