// test-with: ../listings/intvec.c
#include <assert.h>
#include <stdio.h>
#include "intvec.h"

int main(void)
{
    struct intvec v;
    intvec_init(&v);
    assert(v.len == 0 && v.cap == 0 && v.data == NULL);
    long expected_copies = 0;
    for (int i = 0; i < 1000; i++) {
        if (v.len == v.cap)
            expected_copies += (long)v.len;
        assert(intvec_push(&v, i * i) == 0);
    }
    assert(v.len == 1000 && v.cap == 1024);
    assert(v.copies == expected_copies && v.copies == 1023);
    assert(v.copies < 2 * (long)v.len);                     // exercise 10
    for (int i = 0; i < 1000; i++)
        assert(v.data[i] == i * i);
    intvec_free(&v);
    assert(v.len == 0 && v.data == NULL);
    puts("intvec_test: ok");
    return 0;
}
