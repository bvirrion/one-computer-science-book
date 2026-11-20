/* crash.c -- create a file and write 1,500 bytes into it, with the machine stopping after
   each possible number of block writes; after each crash, mount and check. */
// capture: scratch with=minifs.c
#include <stdio.h>
#include "minifs.h"

#ifndef WITH_JOURNAL
#define WITH_JOURNAL 0
#endif

static char data[1500];

static void setup(void)                                /* a file system with one file */
{
    mkfs("crash.img");
    fs_mount("crash.img");
    fs_write(fs_create(ROOT, "notes.txt", T_FILE), 0, "hello\n", 6);
    fs_unmount();
}

static long operation(void)                            /* returns the writes it made */
{
    writes = 0;
    fs_mount("crash.img");
    int ino = fs_create(ROOT, "log.txt", T_FILE);
    if (ino) fs_write(ino, 0, data, sizeof data);
    fs_unmount();
    return writes;
}

int main(void)
{
    journaling = WITH_JOURNAL;
    setup();
    printf("blocks written, %s journal:", journaling ? "with a" : "without");
    show_writes = 1;
    long n = operation();
    show_writes = 0;
    printf("\n");
    for (long k = 1; k < n; k++) {
        setup();
        crash_at = k;                                  /* stop after k writes */
        operation();
        crash_at = 0;
        fs_mount("crash.img");                         /* reboot: replays the journal */
        int ino = fs_lookup(ROOT, "log.txt");
        printf("crash after write %2ld:%s log.txt ", k, replayed ? " replayed," : "");
        if (ino) printf("%u bytes, ", fs_stat(ino).size); else printf("absent, ");
        int problems = fs_check(0);
        printf(problems == 1 ? "1 problem:\n" : problems ? "%d problems:\n" : "consistent\n",
               problems);
        fs_check(1);
        fs_unmount();
    }
    return 0;
}
