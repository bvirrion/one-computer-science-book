// queue.h: the abstract type "queue of int" (first in, first out).
#ifndef QUEUE_H
#define QUEUE_H
#include <stdbool.h>

typedef struct queue queue;

queue *queue_new(void);
void queue_free(queue *q);
bool queue_empty(const queue *q);
void queue_put(queue *q, int x);  // at the rear
int queue_take(queue *q);         // from the front; precondition: not empty
#endif
