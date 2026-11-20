/* aos_soa.c: the mean price of four million books, stored as structures or as arrays. */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define M (1 << 22)

struct book { double price; double weight; long isbn; int pages; int year; char shelf[32]; };

struct books { double *price; double *weight; long *isbn; int *pages; int *year; };

static double now_ms(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

int main(void)
{
    struct book *aos = malloc(sizeof(struct book) * M);       /* 64 bytes per book */
    struct books soa = {malloc(sizeof(double) * M), malloc(sizeof(double) * M),
                        malloc(sizeof(long) * M), malloc(sizeof(int) * M),
                        malloc(sizeof(int) * M)};
    for (long k = 0; k < M; k++) {
        aos[k] = (struct book){.price = (k % 50) + 0.5, .weight = 0.3, .isbn = k,
                               .pages = 200};
        soa.price[k] = (k % 50) + 0.5;
        soa.weight[k] = 0.3, soa.isbn[k] = k, soa.pages[k] = 200, soa.year[k] = 0;
    }
    double t0 = now_ms(), s1 = 0;
    for (long k = 0; k < M; k++)
        s1 += aos[k].price;                   /* 8 useful bytes out of each 64-byte line */
    double t_aos = now_ms() - t0;
    t0 = now_ms();
    double s2 = 0;
    for (long k = 0; k < M; k++)
        s2 += soa.price[k];                   /* every byte of every line is used */
    double t_soa = now_ms() - t0;
    printf("struct size %zu bytes\n", sizeof(struct book));
    printf("array of structures: mean %.2f in %6.2f ms\n", s1 / M, t_aos);
    printf("structure of arrays: mean %.2f in %6.2f ms, %.1f times faster\n", s2 / M, t_soa,
           t_aos / t_soa);
    return 0;
}
