// pbdemo.c: a short session with the phone book (errors 4 and 5 are here).
#include <stdio.h>
#include "phonebook.h"

int main(void)
{
    struct book b;
    book_init(&b, -4);                                    // doubling
    book_add(&b, "Emil Thornworth", 5550101);
    const struct contact *emil = book_find(&b, "Emil Thornworth");
    book_add(&b, "Rosa Yewby", 5550102);
    printf("Emil: %ld\n", emil->number);                  // error 4
    book_add(&b, "Sami Ashworth", 5550103);
    book_add(&b, "Vera Lakewick", 5550104);
    const char *who = book_find(&b, "Rosa Yewby")->name;
    book_remove(&b, "Rosa Yewby");
    printf("removed: first byte %d\n", who[0]);          // error 5
    printf("%zu contacts\n", b.len);
    book_destroy(&b);
    fflush(stdout);
    return 0;
}
