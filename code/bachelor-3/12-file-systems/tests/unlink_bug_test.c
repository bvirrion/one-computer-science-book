/* unlink_bug_test.c: exercise 5. The first unlink leaks the file's blocks; the checker
   finds each one; the corrected unlink leaves the disk consistent. */
#include <assert.h>
#include <stdio.h>
#include "../listings/minifs.c"
#include "../exercises/ex5_unlink_bug.c"

int main(void)
{
    static char data[3000];
    mkfs("u.img");
    fs_mount("u.img");
    fs_write(fs_create(ROOT, "a", T_FILE), 0, data, sizeof data);
    unlink_bug(ROOT, "a");
    assert(fs_check(0) == 3);                          /* three blocks leaked */
    fs_write(fs_create(ROOT, "b", T_FILE), 0, data, sizeof data);
    fs_unlink(ROOT, "b");
    assert(fs_check(0) == 3);                          /* no new leak */
    fs_unmount();
    remove("u.img");
    printf("unlink bug: reproduced\n");
    return 0;
}
