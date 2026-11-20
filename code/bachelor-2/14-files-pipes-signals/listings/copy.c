/* copy.c: copy a file with read and write, b bytes at a time. Usage: copy src dst b */
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc != 4) {
        fprintf(stderr, "usage: copy src dst b\n");
        return 2;
    }
    size_t b = strtoul(argv[3], NULL, 10);
    char *buf = malloc(b);
    int in = open(argv[1], O_RDONLY);
    int out = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (!buf || in < 0 || out < 0) {
        perror("copy");
        return 1;
    }
    ssize_t n;
    while ((n = read(in, buf, b)) > 0)            /* 0 means end of file */
        if (write(out, buf, n) != n) {
            perror("copy: write");
            return 1;
        }
    if (n < 0)
        perror("copy: read");
    close(in);
    close(out);
    return n < 0;
}
