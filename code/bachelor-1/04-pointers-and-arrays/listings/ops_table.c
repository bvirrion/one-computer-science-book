// ops_table.c: a table of functions, chosen by an index.
#include <stdio.h>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }

int main(void)
{
    int (*op[3])(int, int) = {add, sub, mul};     // three pointers to functions
    const char sign[3] = {'+', '-', '*'};
    for (int k = 0; k < 3; k++)
        printf("12 %c 5 = %d\n", sign[k], op[k](12, 5));
    int (*f)(int, int) = mul;
    printf("f(6, 7) = %d, (*f)(6, 7) = %d\n", f(6, 7), (*f)(6, 7));
    return 0;
}
