// capture: cflags=-O0 -fno-stack-protector
// toy_login.c -- the library's login desk, with a bug: the name is copied into a
// 16-byte buffer without checking its length. Built here without the stack protector.
#include <stdio.h>
#include <string.h>

static int check(const char *typed) {
    int is_admin = 0;
    char name[16];
    strcpy(name, typed);  // BUG: no length check
    printf("hello %s\n", name);
    return is_admin;
}

int main(void) {
    char line[256];
    setvbuf(stdout, NULL, _IOLBF, 0);  // print each line at once, even into a pipe
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\n")] = '\0';
        printf("%2zu bytes typed: ", strlen(line));
        printf(check(line) ? "admin desk opened\n" : "reader desk\n");
    }
    return 0;
}
