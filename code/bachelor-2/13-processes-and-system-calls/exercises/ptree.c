/* ptree.c: start a small tree of processes, then print it from /proc, like pstree (exercise 12). */
#define _GNU_SOURCE
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <unistd.h>

struct proc { pid_t pid; char name[32]; };

static void name_of(pid_t pid, char *name, size_t size)
{
    char path[64];
    snprintf(path, sizeof path, "/proc/%d/comm", (int)pid);
    FILE *f = fopen(path, "r");
    snprintf(name, size, "?");
    if (f) {
        if (fgets(name, (int)size, f)) name[strcspn(name, "\n")] = '\0';
        fclose(f);
    }
}

static int by_name(const void *a, const void *b)
{
    return strcmp(((const struct proc *)a)->name, ((const struct proc *)b)->name);
}

static void show(pid_t pid, int depth)
{
    char path[64], name[32], kids[4096] = "";
    name_of(pid, name, sizeof name);
    printf("%*s%s\n", 2 * depth, "", name);
    snprintf(path, sizeof path, "/proc/%d/task/%d/children", (int)pid, (int)pid);
    FILE *f = fopen(path, "r");
    if (f) {
        if (!fgets(kids, sizeof kids, f)) kids[0] = '\0';
        fclose(f);
    }
    struct proc list[64];
    int n = 0;
    for (char *w = strtok(kids, " \n"); w && n < 64; w = strtok(NULL, " \n"))
        list[n++].pid = atoi(w);
    for (int k = 0; k < n; k++)
        name_of(list[k].pid, list[k].name, sizeof list[k].name);
    qsort(list, n, sizeof list[0], by_name);      /* the order of the file is not promised */
    for (int k = 0; k < n; k++)
        show(list[k].pid, depth + 1);
}

static void spawn(const char *name, int ready, int grandchildren)
{
    if (fork() != 0)
        return;
    prctl(PR_SET_NAME, name);                     /* the name /proc/<pid>/comm shows */
    for (int k = 0; k < grandchildren; k++)
        spawn("grandchild", ready, 0);
    if (write(ready, "x", 1) != 1)                /* "I exist, and so do my children" */
        _exit(1);
    pause();                                      /* until the signal at the end */
    _exit(0);
}

int main(void)
{
    int fd[2];
    if (pipe(fd) != 0 || setpgid(0, 0) != 0)      /* our own group, for the final kill */
        return 1;
    prctl(PR_SET_NAME, "ptree");
    spawn("child-b", fd[1], 0);
    spawn("child-a", fd[1], 2);
    char c;
    for (int k = 0; k < 4; k++)                   /* a, b and a's two children are ready */
        if (read(fd[0], &c, 1) != 1)
            return 1;
    show(getpid(), 0);
    signal(SIGTERM, SIG_IGN);                     /* the group signal must spare us */
    kill(0, SIGTERM);
    while (wait(NULL) > 0)
        ;
    return 0;
}
