// er_demo.c: an emergency room; one patient's condition worsens while waiting.
// capture: with=iheap.c
#include "iheap.h"
#include <stdio.h>

int main(void) {
    const char *names[] = {"Ana", "Ben", "Cleo", "Dev", "Eva"};
    int urgency[] = {3, 2, 4, 2, 5};  // 1 is the most urgent
    iheap h;
    ih_init(&h, 5);
    for (int x = 0; x < 5; x++) ih_push(&h, x, urgency[x]);
    printf("next: %s\n", names[ih_pop(&h)]);
    ih_decrease(&h, 4, 1);  // Eva gets worse: urgency 5 -> 1
    printf("Eva's urgency becomes 1; then:");
    while (h.n > 0) printf(" %s", names[ih_pop(&h)]);
    printf("\n");
    ih_free(&h);
    return 0;
}
