// policies.c: three growth policies on the same additions.
// capture: with=phonebook.c
#include <stdio.h>
#include "phonebook.h"

int main(void)
{
    int policy[3] = {16, -4, -3};                       // +16, x2, x1.5
    const char *label[3] = {"+16", "x2", "x1.5"};
    printf("%6s %6s %9s %6s %7s\n", "policy", "n", "copies", "cap", "unused");
    for (long n = 1000; n <= 100000; n *= 10)
        for (int p = 0; p < 3; p++) {
            struct book b;
            book_init(&b, policy[p]);
            for (long i = 0; i < n; i++)
                if (book_add(&b, "Ada", 5550000 + i) != 0)
                    return 1;
            printf("%6s %6ld %9ld %6zu %7zu\n", label[p], n, b.copies, b.cap, b.cap - b.len);
            book_destroy(&b);
        }
    return 0;
}
