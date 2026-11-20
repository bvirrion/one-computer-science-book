// write_text.c: three numbers as text.
// capture: scratch
#include <stdio.h>

int main(void)
{
    int values[3] = {7, 1000, 305419896};
    FILE *f = fopen("numbers.txt", "w");
    if (f == NULL) {
        perror("numbers.txt");
        return 1;
    }
    for (int i = 0; i < 3; i++)
        fprintf(f, "%d\n", values[i]);
    if (fclose(f) != 0) {
        perror("numbers.txt");
        return 1;
    }
    printf("wrote numbers.txt\n");
    return 0;
}
