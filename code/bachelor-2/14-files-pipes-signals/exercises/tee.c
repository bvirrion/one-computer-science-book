/* tee.c: copy standard input to standard output and to every file named (exercise 7).
   Usage: tee [-a] file... */
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define MAXFILES 64

static int write_all(int fd, const char *p, ssize_t n)
{
    while (n > 0) {
        ssize_t w = write(fd, p, n);
        if (w <= 0)
            return -1;
        p += w, n -= w;
    }
    return 0;
}

int main(int argc, char **argv)
{
    int first = 1, flags = O_WRONLY | O_CREAT | O_TRUNC;
    if (argc > 1 && strcmp(argv[1], "-a") == 0) {
        flags = O_WRONLY | O_CREAT | O_APPEND;        /* every write goes to the end */
        first = 2;
    }
    int fds[MAXFILES + 1] = {1}, k = 1, bad = 0;
    for (int i = first; i < argc && k <= MAXFILES; i++) {
        int fd = open(argv[i], flags, 0644);
        if (fd < 0) {
            perror(argv[i]);
            bad = 1;
        } else {
            fds[k++] = fd;
        }
    }
    char buf[4096];
    ssize_t n;
    while ((n = read(0, buf, sizeof buf)) > 0)
        for (int i = 0; i < k; i++)
            if (write_all(fds[i], buf, n) != 0)
                bad = 1;
    for (int i = 1; i < k; i++)
        close(fds[i]);
    return bad || n < 0;
}
