// test-with: ../listings/minish_parse.c ../exercises/andor.c ../exercises/cd_dash.c
/* minish_test.c: the parser, the && / || runner on a fake run, and cd - . */
#define _POSIX_C_SOURCE 200809L
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "minish_parse.h"

int run_list(char **argv, int (*run)(char **));
int cd_builtin(int argc, char **argv);

static char ran[256];

static int fake_run(char **argv)              /* "true" succeeds, anything else fails */
{
    strcat(ran, argv[0]);
    strcat(ran, " ");
    return strcmp(argv[0], "true") == 0 ? 0 : 1;
}

static int list(const char *text)
{
    char line[256], *argv[MAXARGS + 1];
    snprintf(line, sizeof line, "%s", text);
    split(line, argv, MAXARGS, 0);
    ran[0] = '\0';
    return run_list(argv, fake_run);
}

int main(void)
{
    char line[256] = "  echo   two\twords \n", *argv[MAXARGS + 1];
    assert(split(line, argv, MAXARGS, 0) == 3);
    assert(strcmp(argv[0], "echo") == 0 && strcmp(argv[2], "words") == 0 && argv[3] == NULL);
    char blank[] = " \t\n";
    assert(split(blank, argv, MAXARGS, 0) == 0 && argv[0] == NULL);
    char status[] = "echo $? x$?";
    assert(split(status, argv, MAXARGS, 127) == 3);
    assert(strcmp(argv[1], "127") == 0 && strcmp(argv[2], "x$?") == 0);
    char many[] = "a b c d e";
    assert(split(many, argv, 3, 0) == 3 && argv[3] == NULL);

    assert(list("true && echo1") == 1 && strcmp(ran, "true echo1 ") == 0);
    assert(list("false && echo1") == 1 && strcmp(ran, "false ") == 0);
    assert(list("false || true") == 0 && strcmp(ran, "false true ") == 0);
    assert(list("true || echo1") == 0 && strcmp(ran, "true ") == 0);
    assert(list("false && x || true") == 0 && strcmp(ran, "false true ") == 0);
    assert(list("true && false || true && y") == 1 && strcmp(ran, "true false true y ") == 0);

    char start[4096], now[4096];
    assert(getcwd(start, sizeof start));
    char *to_root[] = {"cd", "/", NULL}, *back[] = {"cd", "-", NULL};
    assert(cd_builtin(2, back) == 1);         /* no previous directory yet */
    assert(cd_builtin(2, to_root) == 0 && getcwd(now, sizeof now) && strcmp(now, "/") == 0);
    assert(cd_builtin(2, back) == 0 && getcwd(now, sizeof now) && strcmp(now, start) == 0);
    assert(cd_builtin(2, back) == 0 && getcwd(now, sizeof now) && strcmp(now, "/") == 0);
    char *nowhere[] = {"cd", "/no/such/place", NULL};
    assert(cd_builtin(2, nowhere) == 1 && getcwd(now, sizeof now) && strcmp(now, "/") == 0);
    printf("minish_test: all passed\n");
    return 0;
}
