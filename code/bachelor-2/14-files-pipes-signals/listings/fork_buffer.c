/* fork_buffer.c: a line printed once, appearing twice. */
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    printf("printed once, before the fork\n");   /* stays in the buffer: not a terminal */
    if (fork() == 0)
        return 0;                                 /* the child's exit flushes its copy */
    wait(NULL);
    return 0;                                     /* the parent's exit flushes the original */
}
