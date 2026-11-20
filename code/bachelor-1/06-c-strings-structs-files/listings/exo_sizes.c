// exo_sizes.c: two structures with the same fields.
#include <stdio.h>

struct a {
    char c1;
    int i;
    char c2;
    short s;
};

struct b {
    int i;
    short s;
    char c1;
    char c2;
};

int main(void)
{
    printf("%zu %zu\n", sizeof(struct a), sizeof(struct b));
    return 0;
}
