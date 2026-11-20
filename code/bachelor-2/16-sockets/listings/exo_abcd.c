/* exo_abcd.c: the server sends "ab", then "cd" (exercise 1). */
// shown only: the client's output depends on timing
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>

#include "net.h"

void server_side(int c)
{
    send(c, "ab", 2, 0);
    send(c, "cd", 2, 0);
    close(c);
}

void client_side(int fd)
{
    char buf[3];
    ssize_t n;
    while ((n = recv(fd, buf, sizeof buf, 0)) > 0)
        printf("[%.*s]", (int)n, buf);
    printf("\n");
}
