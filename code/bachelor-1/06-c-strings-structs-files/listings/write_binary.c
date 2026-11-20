// write_binary.c: the same three numbers as the bytes of three int.
// capture: scratch
#include <stdio.h>

int main(void)
{
    int values[3] = {7, 1000, 305419896};
    FILE *f = fopen("numbers.bin", "wb");
    if (f == NULL) {
        perror("numbers.bin");
        return 1;
    }
    size_t written = fwrite(values, sizeof values[0], 3, f);
    printf("position after writing: %ld\n", ftell(f));
    if (fclose(f) != 0 || written != 3) {
        perror("numbers.bin");
        return 1;
    }
    printf("wrote %zu numbers to numbers.bin\n", written);
    return 0;
}
