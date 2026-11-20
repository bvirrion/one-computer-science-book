// env_child.c: what a program receives from the shell that starts it.
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    printf("argc = %d:", argc);
    for (int i = 0; i < argc; i++)
        printf(" [%s]", argv[i]);
    const char *station = getenv("STATION");
    printf("\nSTATION = %s\n", station != NULL ? station : "(not set)");
    return argc - 1;                                    // the exit status: the number of arguments
}
