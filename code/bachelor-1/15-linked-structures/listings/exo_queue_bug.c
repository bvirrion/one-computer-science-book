// exo_queue_bug.c: exercise 6, a queue that forgets one case.
#include <stdio.h>
#include <stdlib.h>

typedef struct cell {
    int value;
    struct cell *next;
} cell;

cell *front = NULL, *rear = NULL;

void put(int x) {
    cell *c = malloc(sizeof *c);
    *c = (cell){x, NULL};
    if (rear == NULL) front = c;
    else rear->next = c;
    rear = c;
}

int take(void) {
    cell *c = front;
    int x = c->value;
    front = c->next;
    free(c);
    return x;
}

int main(void) {
    put(1);
    printf("took %d\n", take());
    put(2);
    put(3);
    printf("front is %s\n", front == NULL ? "NULL" : "a cell");
    return 0;
}
