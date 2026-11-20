// stability.c: heapsort by priority reorders patients of equal priority.
#include <stdio.h>

typedef struct {
    const char *name;
    int priority;  // 1 is the most urgent
} patient;

static void sift_down(patient *a, int n, int i) {  // a max-heap on the priority
    for (int c; (c = 2 * i + 1) < n; i = c) {
        if (c + 1 < n && a[c + 1].priority > a[c].priority) c++;
        if (a[i].priority >= a[c].priority) return;
        patient t = a[i];
        a[i] = a[c], a[c] = t;
    }
}

int main(void) {
    patient a[] = {{"Ana", 2}, {"Ben", 1}, {"Cleo", 2}, {"Dev", 3}, {"Eva", 2}, {"Finn", 1}};
    int n = 6;
    printf("arrival order:");
    for (int i = 0; i < n; i++) printf(" %s(%d)", a[i].name, a[i].priority);
    for (int i = n / 2 - 1; i >= 0; i--) sift_down(a, n, i);
    for (int end = n - 1; end > 0; end--) {
        patient t = a[0];
        a[0] = a[end], a[end] = t;
        sift_down(a, end, 0);
    }
    printf("\nheapsorted:   ");
    for (int i = 0; i < n; i++) printf(" %s(%d)", a[i].name, a[i].priority);
    printf("\n");
    return 0;
}
