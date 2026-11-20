/* sv32.c -- a two-level page table in a byte array, walked as the processor walks it. */
#include <stdio.h>
#include <string.h>
#include "sv32.h"

uint8_t mem[FRAMES * PAGE];
int trace, fault_level;
uint32_t next_frame = 1;               /* frame 0 is never handed out */

uint32_t alloc_frame(void)
{
    memset(mem + next_frame * PAGE, 0, PAGE);
    return next_frame++;
}

static uint32_t *pte_at(uint32_t addr) { return (uint32_t *)(mem + addr); }

#ifndef VPN
#define VPN(va, i) ((i) == 1 ? (va) >> 22 : ((va) >> 12) & 0x3ff)
#endif

void map(uint32_t root, uint32_t va, uint32_t frame, uint32_t flags)
{
    uint32_t *pte = pte_at(root * PAGE + VPN(va, 1) * 4);
    if (!(*pte & PTE_V))                               /* no level-0 table yet */
        *pte = alloc_frame() << 10 | PTE_V;            /* a pointer: R = W = X = 0 */
    uint32_t table = *pte >> 10;
    *pte_at(table * PAGE + VPN(va, 0) * 4) = frame << 10 | flags | PTE_V;
}

int translate(uint32_t root, uint32_t va, char access, uint32_t *pa)
{
    uint32_t a = root * PAGE;
    if (trace)
        printf("%-5s va 0x%08x: vpn1 0x%03x  vpn0 0x%03x  offset 0x%03x\n",
               access == 'r' ? "load" : access == 'w' ? "store" : "fetch",
               va, VPN(va, 1), VPN(va, 0), va & 0xfff);
    for (int i = 1; i >= 0; i--) {
        uint32_t addr = a + VPN(va, i) * 4, pte = *pte_at(addr);
        fault_level = i;
        if (trace)
            printf("  level %d: pte at 0x%05x = 0x%08x", i, addr, pte);
        if (!(pte & PTE_V) || (!(pte & PTE_R) && (pte & PTE_W))) {
            if (trace) printf("  -> not valid: page fault\n");
            return PAGE_FAULT;
        }
        if (!(pte & (PTE_R | PTE_X))) {                /* a pointer to the next level */
            a = (pte >> 10) * PAGE;
            if (trace) printf("  -> table in frame %u\n", pte >> 10);
            continue;
        }
        if (i == 1) {                                  /* a 4 MiB megapage: not used here */
            if (trace) printf("  -> megapage: not supported\n");
            return PAGE_FAULT;
        }
        uint32_t need = access == 'r' ? PTE_R : access == 'w' ? PTE_W : PTE_X;
        if (trace)
            printf("  -> leaf, frame %u, %c%c%c\n", pte >> 10, pte & PTE_R ? 'R' : '-',
                   pte & PTE_W ? 'W' : '-', pte & PTE_X ? 'X' : '-');
        if (!(pte & need)) {
            if (trace) printf("  not allowed: page fault\n");
            return PAGE_FAULT;
        }
        *pte_at(addr) = pte | PTE_A | (access == 'w' ? PTE_D : 0);  /* accessed, dirty */
        *pa = (pte >> 10) * PAGE + (va & 0xfff);
        if (trace) printf("  pa 0x%05x\n", *pa);
        return OK;
    }
    return PAGE_FAULT;                         /* a pointer at level 0: page fault too */
}
