// exo_index.c: two ways of writing the same element.
#include <stdio.h>

int main(void)
{
    int a[4] = {7, 8, 9, 10};
    printf("%d %d %d %d\n", a[2], 2[a], *(a + 2), *(2 + a));
    printf("%c\n", "pointer"[3]);
    return 0;
}
