// overflow.c: a twelve-letter name copied into a ten-byte field.
#include <stdio.h>
#include <string.h>

struct person {
    char name[10];
    int age;
};

int main(void)
{
    struct person p = {"Ann", 19};
    printf("before: %s, age %d\n", p.name, p.age);
    strcpy(p.name, "Christabelle");                    // 12 letters and a zero byte: 13 bytes
    printf("after:  %s, age %d\n", p.name, p.age);
    return 0;
}
