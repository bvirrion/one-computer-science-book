// measure.c: measure DIR QUERIES -- time the index against the naive scan.
#define _POSIX_C_SOURCE 200809L
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "folder.h"
#include "index.h"
#include "query.h"
#include "scan.h"
#include "tokenize.h"

#define MAX_QUERIES 200
#define SCANNED 20  // the naive scan is slow: time it on the first queries only

static double now_ms(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

int main(int argc, char **argv) {
    static char words[MAX_QUERIES][4][MAX_WORD];
    char *terms[MAX_QUERIES][4], line[256];
    int nterms[MAX_QUERIES], nq = 0;
    FILE *q = argc == 3 ? fopen(argv[2], "r") : NULL;
    if (q == NULL) {
        fprintf(stderr, "usage: measure DIR QUERIES\n");
        return 2;
    }
    while (nq < MAX_QUERIES && fgets(line, sizeof line, q) != NULL) {
        char *one[] = {line};
        nterms[nq] = split_words(1, one, words[nq], terms[nq], 4);
        nq++;
    }
    fclose(q);
    double t0 = now_ms();
    Index ix;
    index_init(&ix);
    index_directory(&ix, argv[1]);
    double build = now_ms() - t0;
    Hit a[10], b[10];
    int shown_a, shown_b, same = 1;
    t0 = now_ms();
    for (int rep = 0; rep < 10; rep++)  // all the queries, ten times over
        for (int i = 0; i < nq; i++)
            query_and(&ix, terms[i], nterms[i], a, 10, &shown_a);
    double by_index = (now_ms() - t0) / (10 * nq);
    Folder f;
    folder_list(&f, argv[1]);
    t0 = now_ms();
    for (int i = 0; i < SCANNED; i++)
        scan_and(argv[1], &f, terms[i], nterms[i], b, 10, &shown_b);
    double by_scan = (now_ms() - t0) / SCANNED;
    for (int i = 0; i < SCANNED; i++) {  // and the answers must agree
        int ma = query_and(&ix, terms[i], nterms[i], a, 10, &shown_a);
        int mb = scan_and(argv[1], &f, terms[i], nterms[i], b, 10, &shown_b);
        same = same && ma == mb && shown_a == shown_b && memcmp(a, b, shown_a * sizeof *a) == 0;
    }
    printf("index built in %.1f ms: %d documents, %zu words, %zu bytes\n", build, ix.ndocs,
           ix.nwords, index_memory(&ix));
    printf("one query: %.2f ms scanning the files, %.4f ms with the index\n", by_scan,
           by_index);
    printf("same answers on the first %d queries: %s\n", SCANNED, same ? "yes" : "no");
    printf("the index pays for itself from query %d on\n",
           (int)ceil(build / (by_scan - by_index)));
    folder_free(&f);
    index_free(&ix);
    return 0;
}
