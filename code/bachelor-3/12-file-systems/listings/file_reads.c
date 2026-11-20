/* file_reads.c -- the largest file minifs can hold, and the block reads that reading one
   byte costs at different offsets. */
// capture: scratch with=minifs.c
#include <stdio.h>
#include "minifs.h"

int main(void)
{
    mkfs("reads.img");
    fs_mount("reads.img");
    int ino = fs_create(ROOT, "big", T_FILE);
    char block[BSIZE] = {0};
    long size = 0, n;
    while ((n = fs_write(ino, size, block, BSIZE)) > 0)   /* until the file is full */
        size += n;
    printf("largest file: %ld bytes = (%d direct + %d indirect) blocks of %d bytes\n",
           size, NDIRECT, NPTRS, BSIZE);

    long offsets[] = {0, 9 * 1024 + 1000, 10 * 1024, 100 * 1024, size - 1};
    for (int i = 0; i < 5; i++) {
        char c;
        reads = 0;
        fs_read(ino, offsets[i], &c, 1);
        printf("byte %6ld (file block %3ld): %ld block reads\n", offsets[i],
               offsets[i] / BSIZE, reads);
    }
    fs_unmount();
    return 0;
}
