// queue_list.c: a queue on a singly linked list with a pointer to each end.
#include "queue.h"
#include <stdlib.h>

typedef struct cell {
    int value;
    struct cell *next;
} cell;

struct queue {
    cell *front, *rear;  // both NULL when empty; rear->next == NULL otherwise
};

queue *queue_new(void) {
    queue *q = malloc(sizeof *q);
    if (q == NULL) exit(1);
    q->front = q->rear = NULL;
    return q;
}

bool queue_empty(const queue *q) { return q->front == NULL; }

void queue_put(queue *q, int x) {
    cell *c = malloc(sizeof *c);
    if (c == NULL) exit(1);
    *c = (cell){x, NULL};
    if (q->rear == NULL) q->front = c;  // the queue was empty
    else q->rear->next = c;
    q->rear = c;
}

int queue_take(queue *q) {
    cell *c = q->front;
    int x = c->value;
    q->front = c->next;
    if (q->front == NULL) q->rear = NULL;  // the queue is now empty
    free(c);
    return x;
}

void queue_free(queue *q) {
    while (!queue_empty(q)) queue_take(q);
    free(q);
}
