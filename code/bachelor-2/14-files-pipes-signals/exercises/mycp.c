/* mycp.c: copy src to dst, b bytes at a time, keeping the permission bits; never overwrite
   (exercise 3). Usage: mycp src dst [b] */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc < 3 || argc > 4) {
        fprintf(stderr, "usage: mycp src dst [b]\n");
        return 2;
    }
    size_t b = argc == 4 ? strtoul(argv[3], NULL, 10) : 4096;
    struct stat st;
    int in = open(argv[1], O_RDONLY);
    if (b == 0 || in < 0 || fstat(in, &st) != 0) {
        perror("mycp: source");
        return 1;
    }
    /* O_EXCL: the open fails if dst exists, so nothing is ever overwritten */
    int out = open(argv[2], O_WRONLY | O_CREAT | O_EXCL, st.st_mode & 07777);
    char *buf = malloc(b);
    if (out < 0 || !buf) {
        perror("mycp: destination");
        return 1;
    }
    ssize_t n;
    while ((n = read(in, buf, b)) > 0) {
        for (ssize_t done = 0; done < n;) {       /* write may write less than asked */
            ssize_t w = write(out, buf + done, n - done);
            if (w < 0 && errno != EINTR) {
                perror("mycp: write");
                return 1;
            }
            done += w > 0 ? w : 0;
        }
    }
    fchmod(out, st.st_mode & 07777);              /* the umask may have cleared some bits */
    close(in);
    return close(out) != 0 || n < 0;
}
