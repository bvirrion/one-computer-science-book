// check.h: a minimal unit-test macro that counts failures and goes on.
#ifndef CHECK_H
#define CHECK_H
#include <stdio.h>

static int check_failures = 0, check_count = 0;

#define CHECK(cond)                                                                 \
    do {                                                                            \
        check_count++;                                                              \
        if (!(cond)) {                                                              \
            check_failures++;                                                       \
            fprintf(stderr, "%s:%d: check failed: %s\n", __FILE__, __LINE__, #cond); \
        }                                                                           \
    } while (0)

#define CHECK_REPORT()                                                              \
    (printf("%d checks, %d failed\n", check_count, check_failures), check_failures != 0)

#endif
