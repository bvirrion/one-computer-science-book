// exo_fwrite.c: which bytes does fwrite put in the file?
// capture: scratch
#include <stdio.h>

int main(void)
{
    unsigned int x = 0x12345678;
    FILE *f = fopen("x.bin", "wb");
    if (f == NULL)
        return 1;
    fwrite(&x, sizeof x, 1, f);
    fclose(f);
    return 0;
}
