/* demo_test.c: exercises 1 and 4 on the process of sv32_demo.c. */
#include <assert.h>
#include <stdio.h>
#include "../listings/sv32.c"

int main(void)
{
    uint32_t root = alloc_frame(), pa;
    map(root, 0x00010000, alloc_frame(), PTE_R | PTE_X | PTE_U);
    map(root, 0x10000000, alloc_frame(), PTE_R | PTE_W | PTE_U);
    map(root, 0x7ffff000, alloc_frame(), PTE_R | PTE_W | PTE_U);
    assert(root == 1 && next_frame == 8);
    /* exercise 1: vpn1 0x1ff, vpn0 0x3ff, offset 0x123 */
    assert(*pte_at(0x1000 + 0x1ff * 4) >> 10 == 7);    /* root entry -> table in frame 7 */
    assert(*pte_at(0x7000 + 0x3ff * 4) >> 10 == 6);    /* leaf -> frame 6 */
    assert(translate(root, 0x7ffff123, 'r', &pa) == OK && pa == 0x06123);
    /* exercise 4 */
    assert(translate(root, 0x10001000, 'r', &pa) == PAGE_FAULT && fault_level == 0);
    printf("demo: exercises 1 and 4 hold\n");
    return 0;
}
