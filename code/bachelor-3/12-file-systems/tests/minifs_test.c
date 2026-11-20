/* minifs_test.c: reading back across the indirect boundary, unlink frees everything, the
   journal leaves a consistent disk after a crash at every write, exercises 4 and 8. */
#include <assert.h>
#include <stdio.h>
#include "../listings/minifs.c"

static int free_blocks_count(void)
{
    int n = 0;
    for (int b = DATA; b < NBLOCKS; b++) n += !bit(BBITMAP, b);
    return n;
}

static void crash_run(long k)
{
    static char data[1500];
    mkfs("t.img");
    fs_mount("t.img");
    fs_write(fs_create(ROOT, "notes.txt", T_FILE), 0, "hello\n", 6);
    crash_at = k;
    writes = 0;
    int ino = fs_create(ROOT, "log.txt", T_FILE);
    if (ino) fs_write(ino, 0, data, sizeof data);
    crash_at = 0;
    fs_unmount();
    fs_mount("t.img");
}

int main(void)
{
    static uint8_t pattern[20000], back[20000];
    for (int i = 0; i < 20000; i++) pattern[i] = (uint8_t)(i * 7 + i / 1024);
    mkfs("t.img");
    fs_mount("t.img");
    int before = free_blocks_count() - 1;              /* the root's block comes first */
    int f = fs_create(ROOT, "p", T_FILE);
    assert(fs_write(f, 0, pattern, 20000) == 20000);
    assert(fs_read(f, 0, back, 20000) == 20000 && memcmp(pattern, back, 20000) == 0);
    assert(fs_read(f, 19990, back, 100) == 10);
    assert(fs_check(0) == 0);
    assert(fs_unlink(ROOT, "p") == 0 && fs_lookup(ROOT, "p") == 0);
    assert(free_blocks_count() == before && fs_check(0) == 0);
    /* exercise 8: two reads in the direct region, three behind the indirect block */
    f = fs_create(ROOT, "q", T_FILE);
    fs_write(f, 0, pattern, 20000);
    reads = 0, fs_read(f, 5000, back, 1);
    assert(reads == 2);
    reads = 0, fs_read(f, 15000, back, 1);
    assert(reads == 3);
    fs_unmount();

    /* exercise 4: after fs_demo, unlink notes.txt and create todo.txt */
    mkfs("t.img");
    fs_mount("t.img");
    fs_write(fs_create(ROOT, "notes.txt", T_FILE), 0, "Opening hours: 8:45 to 18:00.\n", 30);
    int src = fs_create(ROOT, "src", T_DIR);
    fs_write(fs_create(src, "main.c", T_FILE), 0, "int main(void) { return 0; }\n", 29);
    fs_write(fs_create(ROOT, "big.dat", T_FILE), 0, pattern, 12288);
    fs_unlink(ROOT, "notes.txt");
    int todo = fs_create(ROOT, "todo.txt", T_FILE);
    fs_write(todo, 0, "tea", 3);
    assert(todo == 2 && fs_stat(todo).direct[0] == 44 && fs_check(0) == 0);
    fs_unmount();

    /* the journal: consistent after a crash at any write */
    journaling = 1;
    for (long k = 1; k < 18; k++) {
        crash_run(k);
        assert(fs_check(0) == 0);
        int ino = fs_lookup(ROOT, "log.txt");
        assert(!ino || fs_stat(ino).size == 0 || fs_stat(ino).size == 1500);
        fs_unmount();
    }
    remove("t.img");
    printf("minifs: all tests passed\n");
    return 0;
}
