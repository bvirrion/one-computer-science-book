/* double_test.c: exercise 6. With the double-indirect pointer, a file of 300 KiB, past the
   10 + 256 blocks of the original inode, is written and read back. */
#define DOUBLE_INDIRECT
#include <assert.h>
#include <stdio.h>
#include "../listings/minifs.c"
#include "../exercises/ex6_double.c"

int main(void)
{
    static uint8_t data[300 * 1024], back[300 * 1024];
    for (long i = 0; i < (long)sizeof data; i++) data[i] = (uint8_t)(i / 1000 + i);
    mkfs("d.img");
    fs_mount("d.img");
    int f = fs_create(ROOT, "big", T_FILE);
    assert(fs_write(f, 0, data, sizeof data) == (long)sizeof data);
    struct inode in = fs_stat(f);
    assert(in.dindirect && in.size == sizeof data);
    assert(fs_read(f, 0, back, sizeof back) == (long)sizeof back);
    assert(memcmp(data, back, sizeof data) == 0);
    reads = 0, fs_read(f, 290 * 1024, back, 1);
    assert(reads == 4);                                /* inode, two pointer blocks, data */
    fs_unmount();
    remove("d.img");
    printf("double indirect: 300 KiB written and read back\n");
    return 0;
}
