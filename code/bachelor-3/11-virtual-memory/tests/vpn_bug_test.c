/* vpn_bug_test.c: exercise 5. With the buggy index, a load from the first kilobyte of a
   mapped page works and a load further in faults; with the right one, both work. */
#include <assert.h>
#include <stdio.h>
#include "../exercises/ex5_vpn_bug.h"
#include "../listings/sv32.c"

int main(void)
{
    uint32_t root = alloc_frame(), pa;
    map(root, 0x10000000, alloc_frame(), PTE_R | PTE_W);
    assert(translate(root, 0x10000004, 'r', &pa) == OK);
    assert(translate(root, 0x10000abc, 'r', &pa) == PAGE_FAULT && fault_level == 0);
    printf("vpn bug: reproduced\n");
    return 0;
}
