// read_number.c: scanf needs to know where to store what it reads (standard input: 45).
#include <stdio.h>

int main(void)
{
    int n;
    if (scanf("%d", &n) != 1) {          // &n: the address of n
        printf("not a number\n");
        return 1;
    }
    printf("%d days = %d weeks and %d days\n", n, n / 7, n % 7);
    return 0;
}
