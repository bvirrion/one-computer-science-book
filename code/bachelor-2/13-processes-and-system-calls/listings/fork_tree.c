/* fork_tree.c: three forks in a row; each process names itself by the forks it was born of. */
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    char name[16] = "p";
    for (int i = 0; i < 3; i++) {
        pid_t r = fork();
        if (r == 0) {                                   /* the child extends its name */
            size_t n = strlen(name);
            name[n] = (char)('0' + i);
            name[n + 1] = '\0';
        } else {
            waitpid(r, NULL, 0);                        /* the child's whole subtree first */
        }
    }
    printf("%-5s depth %zu\n", name, strlen(name) - 1);  /* one digit per fork it came from */
    fflush(stdout);
    return 0;
}
