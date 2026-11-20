// test-with: ../exercises/str_append.c
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "../exercises/str_append.h"

int main(void)
{
    char buf[10] = "Hi";
    assert(str_append(buf, sizeof buf, ", ") == 0 && strcmp(buf, "Hi, ") == 0);
    assert(str_append(buf, sizeof buf, "Ann") == 0 && strcmp(buf, "Hi, Ann") == 0);
    assert(str_append(buf, sizeof buf, "!!") == 0 && strcmp(buf, "Hi, Ann!!") == 0);   // exactly full
    assert(str_append(buf, sizeof buf, "x") == -1 && strcmp(buf, "Hi, Ann!!") == 0);
    char small[4] = "";
    assert(str_append(small, sizeof small, "Christabelle") == -1 && strcmp(small, "Chr") == 0);
    assert(str_append(small, 0, "a") == -1);
    char full[3] = {'a', 'b', 'c'};                     // not terminated
    assert(str_append(full, sizeof full, "d") == -1);
    puts("safe_copy_test: ok");
    return 0;
}
