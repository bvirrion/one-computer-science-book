/* same_inode.c: two names, one file. */
// capture: scratch
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

int main(void)
{
    FILE *f = fopen("first.txt", "w");
    fputs("one file\n", f);
    fclose(f);
    if (link("first.txt", "second.txt") != 0)       /* a second directory entry */
        return 1;
    struct stat s1, s2;
    stat("first.txt", &s1);
    stat("second.txt", &s2);
    int same = s1.st_ino == s2.st_ino && s1.st_dev == s2.st_dev;
    printf("same inode: %s\n", same ? "yes" : "no");
    printf("link count: %ld, size: %ld bytes\n", (long)s1.st_nlink, (long)s1.st_size);
    unlink("first.txt");                             /* remove one name */
    stat("second.txt", &s2);
    printf("after unlink: link count %ld, the file is still there\n", (long)s2.st_nlink);
    return 0;
}
