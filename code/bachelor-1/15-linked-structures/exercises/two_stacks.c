// two_stacks.c: a queue made of two stacks, counting the elementary moves.
#include "stack.h"

typedef struct {
    stack *in, *out;  // the queue is out (top first), then in (bottom first)
    long moves;
} queue2;

void q2_put(queue2 *q, int x) {
    stack_push(q->in, x);
    q->moves++;
}

int q2_take(queue2 *q) {  // precondition: not empty
    if (stack_empty(q->out))
        while (!stack_empty(q->in)) {  // reverse in onto out
            stack_push(q->out, stack_pop(q->in));
            q->moves += 2;
        }
    q->moves++;
    return stack_pop(q->out);
}
