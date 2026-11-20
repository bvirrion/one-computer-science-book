// keyvalue.c: fgets, find the '=', check both lengths, copy.
#include <string.h>
#include "keyvalue.h"

int read_settings(FILE *f, struct setting *s, int max, int *bad_line)
{
    char line[128];
    int n = 0, lineno = 0;
    while (n < max && fgets(line, sizeof line, f) != NULL) {
        lineno++;
        line[strcspn(line, "\n")] = '\0';
        if (line[0] == '\0' || line[0] == '#')
            continue;
        char *eq = strchr(line, '=');
        size_t klen = eq ? (size_t)(eq - line) : 0;
        if (eq == NULL || klen == 0 || klen >= sizeof s[n].key || strlen(eq + 1) >= sizeof s[n].value) {
            *bad_line = lineno;
            return -1;
        }
        memcpy(s[n].key, line, klen);
        s[n].key[klen] = '\0';
        strcpy(s[n].value, eq + 1);                     // fits: checked above
        n++;
    }
    return n;
}
