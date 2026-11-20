// strlen_demo.c: a string is an array of char that ends with a zero byte.
#include <stdio.h>
#include <string.h>

int main(void)
{
    char town[16] = "Brenmoor";
    printf("strlen = %zu, sizeof = %zu\n", strlen(town), sizeof town);
    for (size_t i = 0; i <= strlen(town); i++)
        printf("%4d", town[i]);
    printf("\n");
    town[4] = '\0';                                    // cut the string in the middle
    printf("now \"%s\", strlen = %zu, sizeof = %zu\n", town, strlen(town), sizeof town);
    printf("sizeof \"Brenmoor\" = %zu\n", sizeof "Brenmoor");
    return 0;
}
