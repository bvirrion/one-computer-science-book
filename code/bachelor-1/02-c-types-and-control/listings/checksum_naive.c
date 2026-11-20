// checksum_naive.c: colleague A's checksum of adjacent products, modulo 2^32.
#include <stdint.h>
#include <stdio.h>
#include "temps.h"

uint32_t checksum(const uint16_t *w, int n)
{
    uint32_t s = 0;
    for (int i = 0; i + 1 < n; i++)
        s += w[i] * w[i + 1];            // both operands promoted to int
    return s;
}

int main(int argc, char **argv)
{
    static uint16_t w[1000];
    int n = read_temps(argc > 1 ? argv[1] : "weather.csv", w, 1000);
    printf("%d readings, checksum %u\n", n, checksum(w, n));
    return 0;
}
