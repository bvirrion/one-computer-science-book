// exo_twice.c: a posting list built without looking at its last posting.
#include <math.h>
#include <stdio.h>

typedef struct {
    int doc, count;
} Posting;

int main(void) {
    const int words_of_doc[][4] = {{1, 1, 0, -1}, {2, 1, -1, -1}};  // 0 the, 1 cat, 2 dog
    Posting cat[8];
    int size = 0, ndocs = 2;
    for (int d = 0; d < ndocs; d++)
        for (int i = 0; i < 4 && words_of_doc[d][i] >= 0; i++)
            if (words_of_doc[d][i] == 1)
                cat[size++] = (Posting){d, 1};  // always a new posting
    for (int j = 0; j < size; j++)
        printf("(doc %d, count %d)%s", cat[j].doc, cat[j].count, j + 1 < size ? " " : "\n");
    printf("document frequency of cat: %d, idf: %.3f\n", size, log((double)ndocs / size));
    return 0;
}
