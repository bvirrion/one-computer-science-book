/* zombie.c: a child that has ended but was not waited for, then a child whose parent ended. */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static void nap(void)                                /* one millisecond */
{
    struct timespec t = {0, 1000000};
    nanosleep(&t, NULL);
}

static char state(pid_t pid)                         /* the State letter of /proc/<pid>/status */
{
    char path[64], line[256];
    snprintf(path, sizeof path, "/proc/%d/status", (int)pid);
    FILE *f = fopen(path, "r");
    if (!f) return '-';                              /* no such process any more */
    char s = '?';
    while (fgets(line, sizeof line, f))
        if (strncmp(line, "State:", 6) == 0) s = line[7];
    fclose(f);
    return s;
}

int main(void)
{
    pid_t r = fork();
    if (r == 0) _exit(0);                            /* the child ends at once */
    while (state(r) != 'Z')                          /* until the kernel has marked it */
        nap();
    printf("child ended, not yet waited for: state %c\n", state(r));
    waitpid(r, NULL, 0);
    printf("after waitpid:                   state %c\n", state(r));

    int fd[2];
    if (pipe(fd) != 0) return 1;
    pid_t mid = fork();
    if (mid == 0) {                                  /* the middle process */
        if (fork() == 0) {                           /* the grandchild */
            while (getppid() == mid)                 /* until its parent has ended */
                nap();
            if (write(fd[1], "a", 1) != 1) _exit(1); /* "I was adopted" */
            _exit(0);
        }
        _exit(0);                                    /* ends without waiting for it */
    }
    waitpid(mid, NULL, 0);
    char c;
    if (read(fd[0], &c, 1) == 1)
        printf("the grandchild outlived its parent and was adopted by another process\n");
    return 0;
}
