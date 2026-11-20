/* sv32_demo.c -- a process with a code page, a data page and a stack page, and four
   accesses walked step by step. */
// capture: with=sv32.c
#include <stdio.h>
#include "sv32.h"

int main(void)
{
    uint32_t root = alloc_frame();                     /* the root table: frame 1 */
    map(root, 0x00010000, alloc_frame(), PTE_R | PTE_X | PTE_U);   /* code  */
    map(root, 0x10000000, alloc_frame(), PTE_R | PTE_W | PTE_U);   /* data  */
    map(root, 0x7ffff000, alloc_frame(), PTE_R | PTE_W | PTE_U);   /* stack */
    printf("root table in frame %u; %u frames in use\n\n", root, next_frame - 1);

    trace = 1;
    uint32_t pa;
    translate(root, 0x10000abc, 'r', &pa);             /* a load from the data page */
    translate(root, 0x00010004, 'x', &pa);             /* an instruction fetch */
    translate(root, 0x00010004, 'w', &pa);             /* a store into the code */
    translate(root, 0x40000000, 'r', &pa);             /* nothing mapped there */
    return 0;
}
