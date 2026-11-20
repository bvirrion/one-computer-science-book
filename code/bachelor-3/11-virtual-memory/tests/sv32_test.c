/* sv32_test.c: translations, faults at each level, shared level-0 tables, A and D bits,
   and exercise 4 (an unmapped page next to a mapped one). */
#include <assert.h>
#include <stdio.h>
#include "../listings/sv32.c"

int main(void)
{
    uint32_t root = alloc_frame(), pa;
    uint32_t code = alloc_frame(), data = alloc_frame(), data2 = alloc_frame();
    map(root, 0x00010000, code, PTE_R | PTE_X);
    map(root, 0x10000000, data, PTE_R | PTE_W);
    uint32_t before = next_frame;
    map(root, 0x10002000, data2, PTE_R | PTE_W);       /* same 4 MiB: same level-0 table */
    assert(next_frame == before);
    assert(translate(root, 0x10000abc, 'r', &pa) == OK && pa == data * PAGE + 0xabc);
    assert(translate(root, 0x10002ffc, 'w', &pa) == OK && pa == data2 * PAGE + 0xffc);
    assert(translate(root, 0x00010004, 'x', &pa) == OK && pa == code * PAGE + 4);
    assert(translate(root, 0x00010004, 'w', &pa) == PAGE_FAULT && fault_level == 0);
    assert(translate(root, 0x40000000, 'r', &pa) == PAGE_FAULT && fault_level == 1);
    /* exercise 4: the level-1 entry exists, the level-0 entry is zero */
    assert(translate(root, 0x10001000, 'r', &pa) == PAGE_FAULT && fault_level == 0);
    /* accessed and dirty bits */
    uint32_t table = *pte_at(root * PAGE + (0x10000000 >> 22) * 4) >> 10;
    uint32_t pte = *pte_at(table * PAGE);
    assert((pte & PTE_A) && !(pte & PTE_D));
    translate(root, 0x10000000, 'w', &pa);
    assert(*pte_at(table * PAGE) & PTE_D);
    printf("sv32: all tests passed\n");
    return 0;
}
