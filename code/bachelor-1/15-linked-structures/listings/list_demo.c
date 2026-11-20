// list_demo.c: building and changing a list.
// capture: with=list.c
#include "list.h"
#include <stdio.h>

int main(void) {
    node *head = NULL;  // the empty list
    for (int x = 5; x >= 1; x--) list_push(&head, x);
    list_print(head);
    list_insert_after(head->next, 25);  // after the cell holding 2
    list_print(head);
    list_remove(&head, 1);  // the first cell: head itself changes
    list_remove(&head, 4);
    printf("remove 9: %d\n", list_remove(&head, 9));
    list_print(head);
    printf("length %zu\n", list_length(head));
    list_free(head);
    return 0;
}
