// test-with: ../listings/phonebook.c
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "phonebook.h"

int main(void)
{
    int policies[3] = {16, -4, -3};
    for (int k = 0; k < 3; k++) {
        struct book b;
        book_init(&b, policies[k]);
        char name[16];
        for (int i = 0; i < 500; i++) {
            snprintf(name, sizeof name, "n%d", i);
            assert(book_add(&b, name, i) == 0);
        }
        assert(b.len == 500 && b.cap >= 500);
        if (policies[k] < 0) {
            double r = policies[k] == -4 ? 2.0 : 1.5;
            assert((double)b.copies < r * 500 / (r - 1));          // the growth-factor trade-off
            assert((double)(b.cap - b.len) < (r - 1) * 500);
        }
        assert(book_find(&b, "n123")->number == 123);
        assert(book_remove(&b, "n123") == 0 && book_find(&b, "n123") == NULL);
        assert(book_remove(&b, "n123") == -1 && b.len == 499);
        assert(book_find(&b, "n499")->number == 499);
        book_destroy(&b);
        assert(b.len == 0 && b.items == NULL);
    }
    puts("phonebook_test: ok");
    return 0;
}
