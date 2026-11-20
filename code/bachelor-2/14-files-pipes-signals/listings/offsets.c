/* offsets.c: two opens give two offsets; a dup shares one. */
// capture: scratch
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

static void show(const char *who, int fd)
{
    char c;
    if (read(fd, &c, 1) == 1)
        printf("%-12s read '%c', offset now %ld\n", who, c, (long)lseek(fd, 0, SEEK_CUR));
}

int main(void)
{
    int out = open("abc.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (out < 0 || write(out, "abcdef", 6) != 6) return 1;
    close(out);
    int a = open("abc.txt", O_RDONLY);           /* two opens: two open file descriptions */
    int b = open("abc.txt", O_RDONLY);
    int c = dup(a);                              /* a second descriptor for a's description */
    show("a", a);
    show("a", a);
    show("b", b);
    show("c = dup(a)", c);
    show("a", a);
    return 0;
}
