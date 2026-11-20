// test-with: ../exercises/region_of.c
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../exercises/region_of.h"

int some_global = 3;

int main(void)
{
    int local = 0;
    int *block = malloc(sizeof *block);
    assert(strcmp(region_of(&local, &local), "stack") == 0);
    assert(strcmp(region_of(block, &local), "heap") == 0);
    assert(strcmp(region_of(&some_global, &local), "static data") == 0);
    assert(strcmp(region_of((const void *)&main, &local), "code") == 0);
    free(block);
    puts("region_of_test: ok");
    return 0;
}
