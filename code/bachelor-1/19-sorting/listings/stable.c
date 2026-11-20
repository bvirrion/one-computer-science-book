// stable.c: the library's books sorted by title, then by genre, with a stable sort (merge
// sort) and with an unstable one (heapsort); the poetry shelf of each result.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char title[40], genre[16];
} book;
typedef int (*order)(const book *, const book *);

static int by_title(const book *x, const book *y) { return strcmp(x->title, y->title); }
static int by_genre(const book *x, const book *y) { return strcmp(x->genre, y->genre); }

static void merge_sort(book *a, int n, order cmp, book *tmp) {
    if (n < 2) return;
    int h = n / 2, i = 0, j = h;
    merge_sort(a, h, cmp, tmp);
    merge_sort(a + h, n - h, cmp, tmp);
    for (int k = 0; k < n; k++)  // on a tie, the element of the left half comes first
        tmp[k] = i < h && (j == n || cmp(&a[j], &a[i]) >= 0) ? a[i++] : a[j++];
    memcpy(a, tmp, (size_t)n * sizeof *a);
}

static void sift(book *a, int n, int i, order cmp) {
    for (int c; (c = 2 * i + 1) < n; i = c) {
        if (c + 1 < n && cmp(&a[c], &a[c + 1]) < 0) c++;
        if (cmp(&a[i], &a[c]) >= 0) return;
        book t = a[i];
        a[i] = a[c], a[c] = t;
    }
}

static void heap_sort(book *a, int n, order cmp) {
    for (int i = n / 2 - 1; i >= 0; i--) sift(a, n, i, cmp);
    for (int end = n - 1; end > 0; end--) {
        book t = a[0];
        a[0] = a[end], a[end] = t;
        sift(a, end, 0, cmp);
    }
}

static void poetry(const char *how, const book *a, int n) {
    printf("%s:\n", how);
    for (int i = 0; i < n; i++)
        if (strcmp(a[i].genre, "poetry") == 0) printf("  %s\n", a[i].title);
}

int main(void) {
    static book a[80], b[80], tmp[80];
    FILE *f = fopen("../../../../data/town/books.csv", "r");
    char line[160];
    int n = 0, id;
    if (f == NULL || fgets(line, sizeof line, f) == NULL) return 1;
    while (n < 80 && fgets(line, sizeof line, f) != NULL)
        if (sscanf(line, "%d,%39[^,],%*[^,],%*d,%15[^,]", &id, a[n].title, a[n].genre) == 3) n++;
    fclose(f);
    merge_sort(a, n, by_title, tmp);  // first by title
    memcpy(b, a, sizeof a);
    merge_sort(a, n, by_genre, tmp);  // then by genre: stable, titles stay in order
    heap_sort(b, n, by_genre);        // unstable: the title order is lost
    poetry("merge sort (stable)", a, n);
    poetry("heapsort (not stable)", b, n);
    return 0;
}
