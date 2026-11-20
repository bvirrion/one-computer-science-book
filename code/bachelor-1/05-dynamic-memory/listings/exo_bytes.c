// exo_bytes.c: how many bytes does malloc receive?
#include <stdio.h>

struct reading {
    double value;
    int station;
    char unit;
};

int main(void)
{
    size_t n = 10;
    struct reading *r;
    printf("sizeof *r = %zu, request = %zu bytes\n", sizeof *r, n * sizeof *r);
    return 0;
}
