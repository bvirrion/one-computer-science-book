/* exo_loop.c: an echo server whose loop never ends (exercise 6). */
// capture: with=net.c
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

#include "net.h"

int main(void)
{
    int lfd = tcp_listen(44168);
    if (fork() == 0) {                           /* a client: one line, then goodbye */
        int fd = tcp_connect(44168);
        char echo[8];
        send(fd, "hello", 5, 0);
        recv(fd, echo, sizeof echo, 0);          /* read the echo before closing: no reset */
        close(fd);
        _exit(0);
    }
    int c = accept(lfd, NULL, NULL);
    char buf[64];
    long calls = 0, zeros = 0;
    while (calls < 1000000) {                    /* the bug is inside; this guard is not */
        ssize_t n = recv(c, buf, sizeof buf, 0);
        calls++;
        zeros += n == 0;
        send(c, buf, n > 0 ? n : 0, MSG_NOSIGNAL);
    }
    wait(NULL);
    printf("%ld calls to recv, %ld of them returned 0\n", calls, zeros);
    return 0;
}
