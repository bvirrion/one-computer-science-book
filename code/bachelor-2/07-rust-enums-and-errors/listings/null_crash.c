/* null_crash.c: the same search in C, where "not found" is a null pointer. */
#include <stdio.h>
#include <string.h>

struct book { const char *title; unsigned pages; };

const struct book *find(const struct book *books, int n, const char *title)
{
    for (int i = 0; i < n; i++)
        if (strcmp(books[i].title, title) == 0)
            return &books[i];
    return NULL;                           /* nothing found */
}

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    struct book books[] = {{"The Silent Code", 65}, {"The Paper Forest", 133}};
    printf("%u pages\n", find(books, 2, "The Paper Forest")->pages);
    printf("%u pages\n", find(books, 2, "Seven Comets")->pages);   /* NULL->pages */
    return 0;
}
