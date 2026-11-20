/* fs_demo.c -- make a file system in demo.img, create files and a directory, list them,
   read one back. */
// capture: scratch with=minifs.c
#include <stdio.h>
#include <string.h>
#include "minifs.h"

int main(void)
{
    mkfs("demo.img");
    printf("demo.img: %d blocks of %d bytes\n", NBLOCKS, BSIZE);
    printf("  block 0 superblock, %d inode bitmap, %d block bitmap,\n", IBITMAP, BBITMAP);
    printf("  %d-%d inode table (%d inodes), %d-%d journal, %d-%d data\n", ITABLE,
           ITABLE + ITABLE_BLOCKS - 1, NINODES, JOURNAL, JOURNAL + JOURNAL_BLOCKS - 1,
           DATA, NBLOCKS - 1);

    fs_mount("demo.img");
    const char *text = "Opening hours: 8:45 to 18:00.\n";
    int notes = fs_create(ROOT, "notes.txt", T_FILE);
    fs_write(notes, 0, text, strlen(text));
    int src = fs_create(ROOT, "src", T_DIR);
    int main_c = fs_create(src, "main.c", T_FILE);
    fs_write(main_c, 0, "int main(void) { return 0; }\n", 29);
    static char big[12 * 1024];                        /* 12 KiB: past the 10 direct blocks */
    memset(big, 'x', sizeof big);
    fs_write(fs_create(ROOT, "big.dat", T_FILE), 0, big, sizeof big);

    fs_ls(ROOT, "/");
    fs_ls(src, "/src/");
    char back[64] = {0};
    fs_read(fs_lookup(ROOT, "notes.txt"), 0, back, sizeof back - 1);
    printf("notes.txt: %s", back);
    fs_unmount();
    return 0;
}
