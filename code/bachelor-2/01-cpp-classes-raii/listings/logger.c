// logger.c: append a batch of readings to a log, in C; every check returns early.
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

int append_readings(const char *path, const double *t, int n)
{
    FILE *f = fopen(path, "a");
    if (f == NULL)
        return -1;                       // check 1: cannot open
    char *buf = malloc(16 * (size_t)n + 1);
    if (buf == NULL)
        return -2;                       // check 2: no memory
    int len = 0;
    for (int i = 0; i < n; i++) {
        if (t[i] < -90.0)
            return -3;                   // check 3: an error code in the data
        len += snprintf(buf + len, 16, "%.1f\n", t[i]);
    }
    if (fputs(buf, f) == EOF || fflush(f) == EOF)
        return -4;                       // check 4: the write failed
    free(buf);
    fclose(f);
    return n;
}

int open_files(void)
{
    int n = 0;
    for (int fd = 0; fd < 256; fd++)
        n += fcntl(fd, F_GETFD) != -1;
    return n;
}

int main(void)
{
    double ok[] = {18.5, 19.25, 17.0}, bad[] = {18.5, -99.0, 17.0};
    const char *paths[] = {"no_such_dir/w.log", "/dev/null", "/dev/null", "/dev/full"};
    const double *data[] = {ok, bad, ok, ok};
    for (int s = 0; s < 4; s++) {
        int r = append_readings(paths[s], data[s], 3);
        printf("%-18s returned %2d, open files now %d\n", paths[s], r, open_files());
    }
    return 0;
}
