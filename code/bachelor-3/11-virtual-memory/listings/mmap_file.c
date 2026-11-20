/* mmap_file.c -- a file mapped into memory: ordinary stores change the file. */
// capture: scratch
#include <ctype.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

int main(void)
{
    const char *text = "the print shop opens at nine.\nthe queue forms at ten.\n";
    size_t len = strlen(text);
    int fd = open("notes.txt", O_RDWR | O_CREAT | O_TRUNC, 0644);
    if (write(fd, text, len) != (ssize_t)len) return 1;   /* an ordinary file */

    char *p = mmap(NULL, len, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    close(fd);                                         /* the mapping keeps the file */
    for (size_t i = 0; i < len; i++)                   /* capitalise each sentence */
        if (i == 0 || p[i - 1] == '\n')
            p[i] = (char)toupper((unsigned char)p[i]);
    memcpy(strstr(p, "nine"), "8:45", 4);              /* no write(): just stores */
    msync(p, len, MS_SYNC);
    munmap(p, len);

    char back[128] = {0};
    fd = open("notes.txt", O_RDONLY);
    ssize_t n = read(fd, back, sizeof back - 1);
    close(fd);
    printf("read back %zd bytes:\n%s", n, back);
    return 0;
}
