// test-with: ../listings/pipeline_lib.c ../exercises/capture_cmd.c
/* pipeline_test.c: run_pipeline's statuses and data, through capture(); capture() itself. */
#define _POSIX_C_SOURCE 200809L
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "pipeline.h"

char *capture(char *const argv[], const char *input, int *status);

int main(void)
{
    int s;
    char *cat[] = {"cat", NULL}, *sh[] = {"sh", "-c", "exit 3", NULL};
    char *out = capture(cat, "abc\n", &s);
    assert(out && strcmp(out, "abc\n") == 0 && s == 0);
    free(out);
    out = capture(sh, "", &s);
    assert(out && out[0] == '\0' && s == 3);
    free(out);
    char *big = malloc(300001);                   /* more than a pipe holds: no deadlock */
    memset(big, 'y', 300000);
    big[300000] = '\0';
    char *wc[] = {"wc", "-c", NULL};
    out = capture(wc, big, &s);
    assert(out && atoi(out) == 300000 && s == 0);
    free(out), free(big);

    /* run_pipeline from a child whose stdout is a file, then read the file */
    char *seq[] = {"seq", "1", "10", NULL}, *tac[] = {"tac", NULL}, *head[] = {"head", "-3", NULL};
    char **const st[] = {seq, tac, head};
    char *fls[] = {"false", NULL}, *tru[] = {"true", NULL};
    char **const last_false[] = {tru, fls}, **const last_true[] = {fls, tru};
    char path[] = "/tmp/pipeline_testXXXXXX";
    int fd = mkstemp(path);
    int saved = dup(1);
    dup2(fd, 1);
    int r1 = run_pipeline(st, 3);
    int r2 = run_pipeline(last_false, 2), r3 = run_pipeline(last_true, 2);
    char *one[] = {"echo", "alone", NULL};
    char **const single[] = {one};
    int r4 = run_pipeline(single, 1);
    fflush(stdout);
    dup2(saved, 1);
    char buf[128] = "";
    lseek(fd, 0, SEEK_SET);
    ssize_t n = read(fd, buf, sizeof buf - 1);
    buf[n > 0 ? n : 0] = '\0';
    close(fd), unlink(path);
    assert(r1 == 0 && r2 == 1 && r3 == 0 && r4 == 0);
    assert(strcmp(buf, "10\n9\n8\nalone\n") == 0);
    printf("pipeline_test: all passed\n");
    return 0;
}
