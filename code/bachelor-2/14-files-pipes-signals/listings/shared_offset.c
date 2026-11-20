/* shared_offset.c: after fork, parent and child share the offset of an open file. */
// capture: scratch
#include <fcntl.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    int fd = open("log.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fork() == 0) {
        if (write(fd, "child line\n", 11) != 11) _exit(1);
        _exit(0);
    }
    wait(NULL);                                  /* the child has written 11 bytes */
    if (write(fd, "parent line\n", 12) != 12) return 1;   /* goes after them, not over them */
    close(fd);
    char buf[64];
    fd = open("log.txt", O_RDONLY);
    ssize_t n = read(fd, buf, sizeof buf);
    printf("log.txt holds %zd bytes:\n%.*s", n, (int)n, buf);
    return 0;
}
