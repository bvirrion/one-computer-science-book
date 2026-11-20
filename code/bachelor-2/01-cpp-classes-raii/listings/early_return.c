// early_return.c: an early return forgets to close a file.
#include <fcntl.h>
#include <stdio.h>
#include <string.h>

// The version number of a log whose first line is "LOG v<n> ...", or -1.
int header_version(const char *path)
{
    FILE *f = fopen(path, "r");
    if (f == NULL)
        return -1;
    char line[128];
    if (fgets(line, sizeof line, f) == NULL)
        return -1;                       // leaves f open
    if (strncmp(line, "LOG v", 5) != 0)
        return -1;                       // leaves f open
    int version = line[5] - '0';
    fclose(f);
    return version;
}

int open_files(void)                     // counts the open descriptors 0..255
{
    int n = 0;
    for (int fd = 0; fd < 256; fd++)
        if (fcntl(fd, F_GETFD) != -1)
            n++;
    return n;
}

int main(void)
{
    printf("open files at start: %d\n", open_files());
    printf("good.log: version %d\n", header_version("good.log"));
    for (int i = 0; i < 10; i++)
        header_version("bad.log");
    printf("bad.log read 10 times: version -1 each time\n");
    printf("open files at end:   %d\n", open_files());
    return 0;
}
