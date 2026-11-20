// exo_ring_bug.c: exercise 5, a ring buffer kept as two indices, head and tail.
#include <stdio.h>

enum { N = 4 };
int data[N];
int head = 0, tail = 0;  // the queue is data[head..tail), modulo N

int empty(void) { return head == tail; }
void put(int x) { data[tail] = x; tail = (tail + 1) % N; }
int take(void) { int x = data[head]; head = (head + 1) % N; return x; }

int main(void) {
    for (int x = 1; x <= 4; x++) put(x);
    printf("after four puts, empty() says %d\n", empty());
    int n = 0;
    while (!empty()) n++, take();
    printf("taken: %d elements\n", n);
    return 0;
}
