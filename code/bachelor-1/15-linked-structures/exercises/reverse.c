// reverse.c: reverse a singly linked list in place, in one pass.
#include "list.h"

node *list_reverse(node *head) {
    node *done = NULL;  // invariant: done is the reversed prefix, head the rest
    while (head != NULL) {
        node *next = head->next;
        head->next = done;
        done = head;
        head = next;
    }
    return done;
}
