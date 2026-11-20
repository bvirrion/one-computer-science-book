// capture: cflags=-O0 -fno-stack-protector
// toy_login_fixed.c -- the same desk with the length checked before the copy, built
// like toy_login.c, without the stack protector: the check alone makes it safe.
#include <stdio.h>
#include <string.h>

static int check(const char *typed) {
    int is_admin = 0;
    char name[16];
    if (strlen(typed) >= sizeof name) {  // the name and its final '\0' must fit
        printf("name too long, refused\n");
        return 0;
    }
    strcpy(name, typed);
    printf("hello %s\n", name);
    return is_admin;
}

int main(void) {
    char line[256];
    setvbuf(stdout, NULL, _IOLBF, 0);
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\n")] = '\0';
        printf("%2zu bytes typed: ", strlen(line));
        printf(check(line) ? "admin desk opened\n" : "reader desk\n");
    }
    return 0;
}
