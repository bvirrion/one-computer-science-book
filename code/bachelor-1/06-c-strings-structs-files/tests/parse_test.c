// test-with: ../exercises/read_int.c ../exercises/keyvalue.c
#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include "../exercises/keyvalue.h"
#include "../exercises/read_int.h"

int main(void)
{
    struct { const char *s; int ok; int v; } cases[] = {
        {"42", 0, 42}, {"  -7\n", 0, -7}, {"+15 ", 0, 15}, {"2147483647", 0, INT_MAX},
        {"-2147483648", 0, INT_MIN}, {"", -1, 0}, {"   ", -1, 0}, {"abc", -1, 0}, {"12x", -1, 0},
        {"4.5", -1, 0}, {"2147483648", -1, 0}, {"99999999999999999999", -1, 0}, {"1 2", -1, 0},
    };
    for (size_t i = 0; i < sizeof cases / sizeof cases[0]; i++) {
        int v = 12345;
        int r = read_int(cases[i].s, &v);
        assert(r == cases[i].ok);
        assert(v == (r == 0 ? cases[i].v : 12345));
    }
    const char *text = "# town settings\nname=Brenmoor\n\nstations=2\nunit=mm\n";
    FILE *f = tmpfile();
    fputs(text, f);
    rewind(f);
    struct setting s[4];
    int bad = 0;
    assert(read_settings(f, s, 4, &bad) == 3);
    assert(strcmp(s[0].key, "name") == 0 && strcmp(s[0].value, "Brenmoor") == 0);
    assert(strcmp(s[2].key, "unit") == 0 && strcmp(s[2].value, "mm") == 0);
    fclose(f);
    const char *broken = "a=1\nno equals sign\n";
    f = tmpfile();
    fputs(broken, f);
    rewind(f);
    assert(read_settings(f, s, 4, &bad) == -1 && bad == 2);
    fclose(f);
    puts("parse_test: ok");
    return 0;
}
