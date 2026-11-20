// shadow.c: one name, three variables.
#include <stdio.h>

int level = 1;                           // global: file scope

void show(void)
{
    printf("in show:     level = %d\n", level);
}

int main(void)
{
    int level = 2;                       // hides the global inside main
    {
        int level = 3;                   // hides main's level inside this block
        printf("inner block: level = %d\n", level);
    }
    printf("in main:     level = %d\n", level);
    show();
    return 0;
}
