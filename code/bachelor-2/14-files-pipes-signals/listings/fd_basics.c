/* fd_basics.c: open, write, close, then open again and read in small pieces. */
// capture: scratch
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int main(void)
{
    int fd = open("notes.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    printf("open for writing gave descriptor %d\n", fd);      /* 0, 1, 2 are taken */
    ssize_t w = write(fd, "returned: 3 books", 17);
    printf("write returned %zd\n", w);
    close(fd);

    fd = open("notes.txt", O_RDONLY);
    printf("open for reading gave descriptor %d\n", fd);      /* 3 is free again */
    char buf[8];
    ssize_t n;
    while ((n = read(fd, buf, sizeof buf)) > 0)               /* at most 8 bytes each time */
        printf("read returned %zd: \"%.*s\"\n", n, (int)n, buf);
    printf("read returned %zd: end of file\n", n);
    close(fd);
    return 0;
}
