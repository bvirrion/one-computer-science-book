/* ex5_vpn_bug.h -- the walk's index into the page tables, as first written. */
#define VPN(va, i) ((i) == 1 ? (va) >> 22 : ((va) >> 10) & 0x3ff)
