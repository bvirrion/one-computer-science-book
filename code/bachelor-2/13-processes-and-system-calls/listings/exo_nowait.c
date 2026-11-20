/* exo_nowait.c: a parent that never waits (exercise 2). */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static int zombies(void)                             /* children of this process in state Z */
{
    char path[64], buf[4096], line[256];
    snprintf(path, sizeof path, "/proc/%d/task/%d/children", (int)getpid(), (int)getpid());
    FILE *f = fopen(path, "r");
    if (!f || !fgets(buf, sizeof buf, f)) buf[0] = '\0';
    if (f) fclose(f);
    int n = 0;
    for (char *w = strtok(buf, " \n"); w; w = strtok(NULL, " \n")) {
        snprintf(path, sizeof path, "/proc/%s/status", w);
        FILE *s = fopen(path, "r");
        while (s && fgets(line, sizeof line, s))
            n += strncmp(line, "State:\tZ", 8) == 0;
        if (s) fclose(s);
    }
    return n;
}

int main(void)
{
    for (int k = 0; k < 3; k++)
        if (fork() == 0)
            _exit(0);                                /* each child ends at once */
    struct timespec t = {0, 1000000};
    while (zombies() < 3)
        nanosleep(&t, NULL);
    printf("3 children ended, %d of them still in the process table\n", zombies());
    return 0;
}
