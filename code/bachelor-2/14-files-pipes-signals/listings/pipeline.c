/* pipeline.c: the hook's word count, run by a C program instead of a shell. */
// capture: with=pipeline_lib.c
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

#include "pipeline.h"

int main(void)
{
    char *tr1[] = {"tr", "-cs", "A-Za-z", "\n", NULL};
    char *tr2[] = {"tr", "A-Z", "a-z", NULL};
    char *sort1[] = {"sort", NULL};
    char *uniq[] = {"uniq", "-c", NULL};
    char *sort2[] = {"sort", "-rn", NULL};
    char *head[] = {"head", "-6", NULL};
    char **const stages[] = {tr1, tr2, sort1, uniq, sort2, head};
    int in = open("words.txt", O_RDONLY);         /* the first stage reads the text */
    dup2(in, 0);
    close(in);
    int status = run_pipeline(stages, 6);
    printf("6 processes, 5 pipes; the last stage exited with %d\n", status);
    return 0;
}
