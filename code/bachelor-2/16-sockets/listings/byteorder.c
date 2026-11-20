/* byteorder.c: the bytes of a number in this machine's memory and in network order. */
#include <arpa/inet.h>
#include <stdint.h>
#include <stdio.h>

static void bytes(const char *what, const void *p, int n)
{
    printf("%-26s", what);
    for (int i = 0; i < n; i++)
        printf(" %02x", ((const unsigned char *)p)[i]);
    printf("\n");
}

int main(void)
{
    uint32_t x = 0x0a0b0c0d, nx = htonl(x);
    uint16_t port = 44160, nport = htons(port);  /* 44160 = 0xac80 */
    bytes("0x0a0b0c0d in memory:", &x, 4);
    bytes("htonl(0x0a0b0c0d):", &nx, 4);
    bytes("port 44160 in memory:", &port, 2);
    bytes("htons(44160):", &nport, 2);
    printf("ntohs(htons(44160)) = %u\n", (unsigned)ntohs(nport));
    return 0;
}
