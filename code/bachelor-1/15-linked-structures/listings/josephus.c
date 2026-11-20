// josephus.c: n people in a circle, every k-th leaves; who remains?
#include <stdio.h>
#include <stdlib.h>

typedef struct person {
    int number;
    struct person *next;
} person;

// simulation on a circular singly linked list; people numbered from 1
static int simulate(int n, int k, int show) {
    person *people = malloc(n * sizeof *people);
    for (int i = 0; i < n; i++) people[i] = (person){i + 1, &people[(i + 1) % n]};
    person *before = &people[n - 1];  // the person before the next one to count
    for (int left = n; left > 1; left--) {
        for (int step = 1; step < k; step++) before = before->next;
        if (show) printf("%d ", before->next->number);
        before->next = before->next->next;  // the k-th leaves the circle
    }
    int last = before->number;
    free(people);
    return last;
}

static int recurrence(int n, int k) {  // J(1) = 0, J(n) = (J(n - 1) + k) mod n, from 0
    int j = 0;
    for (int m = 2; m <= n; m++) j = (j + k) % m;
    return j + 1;
}

static int closed_form(int n) {  // k = 2: 2(n - 2^floor(log2 n)) + 1
    int p = 1;
    while (2 * p <= n) p *= 2;
    return 2 * (n - p) + 1;
}

int main(void) {
    printf("n = 10, k = 3, leaving: ");
    int last = simulate(10, 3, 1);
    printf("-> %d remains\n", last);
    printf("%4s %10s %10s %12s\n", "n", "simulated", "recurrence", "closed form");
    for (int n = 1; n <= 16; n++)
        printf("%4d %10d %10d %12d\n", n, simulate(n, 2, 0), recurrence(n, 2),
               closed_form(n));
    int bad = 0;
    for (int n = 1; n <= 10000; n++) bad += simulate(n, 2, 0) != closed_form(n);
    printf("k = 2, n <= 10000: simulation and closed form disagree %d times\n", bad);
    bad = 0;
    for (int n = 1; n <= 1000; n++)
        for (int k = 1; k <= 7; k++) bad += simulate(n, k, 0) != recurrence(n, k);
    printf("k <= 7, n <= 1000: simulation and recurrence disagree %d times\n", bad);
    return 0;
}
