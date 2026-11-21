// where.c: six objects; in which region of the running program is each one?
#include <stdlib.h>

const char *motto = "keep it simple";   // (a) motto, (b) the characters
int table[1000];                        // (c)
int limit = 10;                         // (d)

int main(void)
{
    int depth = 0;                      // (e)
    char *buffer = malloc(64);          // (f) the 64 bytes
    if (buffer == NULL)
        return 1;
    buffer[0] = (char)(depth + limit + table[0] + motto[0]);
    free(buffer);
    return 0;
}
