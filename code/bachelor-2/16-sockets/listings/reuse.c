/* reuse.c: bind a port again right after a server closed a connection (exercise 12). */
// capture: with=net.c
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "net.h"

static int bind_again(int reuse)
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof reuse);
    struct sockaddr_in a = {0};
    a.sin_family = AF_INET;
    a.sin_port = htons(44169);
    a.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    int r = bind(fd, (struct sockaddr *)&a, sizeof a);
    printf("bind with SO_REUSEADDR = %d: %s\n", reuse, r == 0 ? "ok" : strerror(errno));
    close(fd);
    return r;
}

int main(void)
{
    int lfd = tcp_listen(44169);                 /* with SO_REUSEADDR, as always */
    int cfd = tcp_connect(44169);
    int c = accept(lfd, NULL, NULL);
    close(c);                                    /* the server closes first ... */
    char b;
    recv(cfd, &b, 1, 0);                         /* (the client sees end of stream) */
    close(cfd);
    close(lfd);                                  /* ... and the server program ends */
    bind_again(0);                               /* its connection is in TIME_WAIT */
    bind_again(1);
    return 0;
}
