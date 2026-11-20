// phonebook.h: a growable list of contacts.
// Convention: the book owns the names it stores. book_add copies the name it is given;
// book_remove and book_destroy free the names they drop. A pointer returned by book_find
// is borrowed: the caller must not free it, and it is valid only until the next
// book_add or book_remove.
#ifndef PHONEBOOK_H
#define PHONEBOOK_H
#include <stddef.h>

struct contact {
    char *name;
    long number;
};

struct book {
    struct contact *items;      // a heap block of cap contacts, len of them used
    size_t len, cap;
    int policy;                 // > 0: add `policy` slots; -4: double; -3: multiply by 1.5
    long copies;                // contacts copied by the growths
};

void book_init(struct book *b, int policy);
int book_add(struct book *b, const char *name, long number);
const struct contact *book_find(const struct book *b, const char *name);
int book_remove(struct book *b, const char *name);
void book_destroy(struct book *b);

#endif
