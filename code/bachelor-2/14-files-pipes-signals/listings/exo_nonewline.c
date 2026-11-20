/* exo_nonewline.c: a printf without a newline, then a fork (exercise 5). */
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    printf("A");
    pid_t r = fork();
    printf("B\n");
    if (r > 0)
        wait(NULL);
    return 0;
}
