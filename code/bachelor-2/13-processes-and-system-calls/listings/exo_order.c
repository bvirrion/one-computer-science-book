/* exo_order.c: in which order are the letters printed? (exercise 5) */
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *s)
{
    printf("%s", s);
    fflush(stdout);
}

int main(void)
{
    say("A");
    pid_t r = fork();
    if (r == 0) {
        say("B");
        if (fork() == 0) {
            say("C");
            return 0;
        }
        wait(NULL);
        say("D");
        return 0;
    }
    waitpid(r, NULL, 0);
    say("E");
    if (fork() == 0) {
        say("F");
        return 0;
    }
    wait(NULL);
    say("G\n");
    return 0;
}
