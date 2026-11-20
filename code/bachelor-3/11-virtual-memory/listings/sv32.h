/* sv32.h -- Sv32 address translation over a simulated physical memory of 1 MiB. */
#include <stdint.h>

#define PAGE 4096u
#define FRAMES 256u                    /* 1 MiB of physical memory: 256 frames */
#define PTE_V 0x01u                    /* the bits 0..7 of a page-table entry */
#define PTE_R 0x02u
#define PTE_W 0x04u
#define PTE_X 0x08u
#define PTE_U 0x10u
#define PTE_A 0x40u
#define PTE_D 0x80u

enum { OK, PAGE_FAULT };

extern uint8_t mem[FRAMES * PAGE];
extern int trace;                      /* print each step of the walk */
extern int fault_level;                /* the level at which the last walk stopped */
extern uint32_t next_frame;            /* frames 1 .. next_frame - 1 are in use */

uint32_t alloc_frame(void);
void map(uint32_t root, uint32_t va, uint32_t frame, uint32_t flags);
int translate(uint32_t root, uint32_t va, char access, uint32_t *pa);
