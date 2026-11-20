// test-with: ../listings/queue_list.c ../listings/stack_list.c ../exercises/two_stacks.c
// The linked queue and the queue of two stacks, against an array model; the moves of
// the second stay below 4 per operation (the amortised bound of exercise 12).
#include "queue.h"
#include "stack.h"
#include <assert.h>
#include <stdio.h>

typedef struct { stack *in, *out; long moves; } queue2;
void q2_put(queue2 *q, int x);
int q2_take(queue2 *q);

int main(void) {
    queue *q = queue_new();
    queue2 q2 = {stack_new(), stack_new(), 0};
    static int model[100000];
    int front = 0, back = 0;
    unsigned state = 11;
    long ops = 0;
    for (int i = 0; i < 100000; i++, ops++) {
        state = state * 1103515245u + 12345u;
        if (front == back || (state >> 16) % 5 < 3) {
            queue_put(q, i), q2_put(&q2, i), model[back++] = i;
        } else {
            int x = model[front++];
            assert(queue_take(q) == x && q2_take(&q2) == x);
        }
        assert(queue_empty(q) == (front == back));
        assert(q2.moves <= 4 * (ops + 1));
    }
    queue_free(q);
    stack_free(q2.in), stack_free(q2.out);
    puts("queues: ok");
    return 0;
}
