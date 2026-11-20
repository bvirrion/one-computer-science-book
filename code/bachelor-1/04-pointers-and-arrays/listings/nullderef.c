// nullderef.c: following the null pointer.
#include <stdio.h>

int main(int argc, char **argv)
{
    int *p = NULL;
    if (argc > 5)                        // never true here: p stays NULL
        p = (int *)argv;
    printf("about to read *p\n");
    fflush(stdout);
    printf("*p = %d\n", *p);
    return 0;
}
