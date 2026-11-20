/* sv32_ex4.c -- exercise 4: the process of sv32_demo.c, and a load from 0x10001000. */
// capture: with=sv32.c
#include "sv32.h"

int main(void)
{
    uint32_t root = alloc_frame(), pa;
    map(root, 0x00010000, alloc_frame(), PTE_R | PTE_X | PTE_U);
    map(root, 0x10000000, alloc_frame(), PTE_R | PTE_W | PTE_U);
    map(root, 0x7ffff000, alloc_frame(), PTE_R | PTE_W | PTE_U);
    trace = 1;
    translate(root, 0x10001000, 'r', &pa);
    return 0;
}
