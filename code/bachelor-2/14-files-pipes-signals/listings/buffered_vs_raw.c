/* buffered_vs_raw.c: copy 4 MiB with buffers of 1 byte to 64 KiB; and putc against write. */
// capture: scratch
#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define SIZE (4L << 20)

static double now_ms(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

int main(void)
{
    char *data = malloc(SIZE);
    for (long k = 0; k < SIZE; k++)
        data[k] = (char)('a' + k % 26);
    int fd = open("big.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (write(fd, data, SIZE) != SIZE) return 1;
    close(fd);
    char *buf = malloc(65536);
    printf("%8s %10s %10s\n", "b", "reads", "ms");
    for (long b = 1; b <= 65536; b *= 4) {
        int in = open("big.txt", O_RDONLY);
        int out = open("copy.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
        long reads = 0;
        double t0 = now_ms();
        ssize_t n;
        do {
            n = read(in, buf, b);
            reads++;
            if (n > 0 && write(out, buf, n) != n) return 1;
        } while (n > 0);
        printf("%8ld %10ld %10.1f\n", b, reads, now_ms() - t0);
        close(in), close(out);
    }
    FILE *f = fopen("copy.txt", "w");
    double t0 = now_ms();
    for (long k = 0; k < SIZE; k++)
        putc(data[k], f);                   /* the library's buffer, one byte at a time */
    fclose(f);
    printf("putc, one byte at a time:  %8.1f ms\n", now_ms() - t0);
    return 0;
}
