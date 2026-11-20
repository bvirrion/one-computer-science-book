// test-with: ../exercises/my_strdup.c
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../exercises/my_strdup.h"

int main(void)
{
    const char *words[] = {"", "a", "Brenmoor", "Emil Thornworth"};
    for (int i = 0; i < 4; i++) {
        char *c = my_strdup(words[i]);
        assert(c != NULL && c != words[i]);
        assert(strcmp(c, words[i]) == 0);
        c[0] = 'X';                                      // the copy is writable and separate
        assert(words[i][0] != 'X');
        free(c);
    }
    puts("strdup_test: ok");
    return 0;
}
