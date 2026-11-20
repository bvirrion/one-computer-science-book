/* kmp_bench.c: naive search against KMP on the worst text for the naive one:
   the text a...a, the pattern a...ab of m letters (no occurrence). */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static long naive(const char *t, long n, const char *p, long m, long *cmp) {
    long found = 0;
    for (long s = 0; s + m <= n; s++) {
        long j = 0;
        while (j < m && (++*cmp, t[s + j] == p[j])) j++;
        if (j == m) found++;
    }
    return found;
}

static long kmp(const char *t, long n, const char *p, long m, long *cmp) {
    long *pi = calloc(m + 1, sizeof *pi), found = 0, q = 0;
    for (long k = 0, i = 2; i <= m; i++) {  /* the failure function */
        while (k > 0 && p[k] != p[i - 1]) k = pi[k];
        if (p[k] == p[i - 1]) k++;
        pi[i] = k;
    }
    for (long i = 0; i < n; i++) {
        for (;;) {
            if (i - q > n - m) goto done;  /* the pattern no longer fits */
            ++*cmp;
            if (p[q] == t[i]) { q++; break; }
            if (q == 0) break;
            q = pi[q];
        }
        if (q == m) { found++; q = pi[q]; }
    }
done:
    free(pi);
    return found;
}

static double best_ms(long (*f)(const char *, long, const char *, long, long *),
                      const char *t, long n, const char *p, long m, long *cmp) {
    double best = 1e30;
    for (int r = 0; r < 3; r++) {
        struct timespec a, b;
        *cmp = 0;
        clock_gettime(CLOCK_MONOTONIC, &a);
        if (f(t, n, p, m, cmp) != 0) puts("unexpected occurrence");
        clock_gettime(CLOCK_MONOTONIC, &b);
        double ms = (b.tv_sec - a.tv_sec) * 1e3 + (b.tv_nsec - a.tv_nsec) / 1e6;
        if (ms < best) best = ms;
    }
    return best;
}

int main(void) {
    const long m = 100;
    char *p = malloc(m + 1);
    memset(p, 'a', m - 1);
    p[m - 1] = 'b';
    p[m] = 0;
    printf("       n   naive comparisons  naive (ms)   KMP comparisons  KMP (ms)\n");
    for (long n = 200000; n <= 1600000; n += 200000) {
        char *t = malloc(n);
        memset(t, 'a', n);
        long c1, c2;
        double t1 = best_ms(naive, t, n, p, m, &c1), t2 = best_ms(kmp, t, n, p, m, &c2);
        printf("%8ld %19ld %11.2f %17ld %9.2f\n", n, c1, t1, c2, t2);
        free(t);
    }
    free(p);
    return 0;
}
