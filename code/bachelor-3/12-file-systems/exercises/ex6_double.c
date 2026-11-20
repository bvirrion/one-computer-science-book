/* ex6_double.c -- exercise 6: the double-indirect pointer. Block k of its region is entry
   k % NPTRS of the indirect block named by entry k / NPTRS of the double-indirect block. */
static uint32_t bmap_double(struct inode *in, uint32_t k, int *fresh)
{
    if (k >= NPTRS * NPTRS) return 0;                  /* beyond the largest file */
    if (!in->dindirect && (!fresh || !(in->dindirect = new_block(1)))) return 0;
    uint32_t outer[NPTRS], inner[NPTRS];
    get(in->dindirect, outer);
    uint32_t mid = outer[k / NPTRS];
    if (!mid) {
        if (!fresh || !(mid = new_block(1))) return 0;
        outer[k / NPTRS] = mid;
        put(in->dindirect, outer);
    }
    get(mid, inner);
    uint32_t leaf = inner[k % NPTRS];
    if (!leaf && fresh && (leaf = new_block(0))) {
        inner[k % NPTRS] = leaf;
        put(mid, inner);
        *fresh = 1;
    }
    return leaf;
}
