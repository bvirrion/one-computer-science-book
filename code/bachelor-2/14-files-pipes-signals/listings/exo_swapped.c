/* exo_swapped.c: a redirection with the arguments of dup2 swapped (exercise 6). */
// capture: scratch
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    if (fork() == 0) {
        int fd = open("out.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
        dup2(1, fd);                              /* meant: dup2(fd, 1) */
        close(fd);
        execlp("echo", "echo", "meant for out.txt", (char *)NULL);
        _exit(127);
    }
    wait(NULL);
    struct stat st;
    stat("out.txt", &st);
    printf("out.txt has %ld bytes\n", (long)st.st_size);
    return 0;
}
