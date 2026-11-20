/* boundaries.c: three sends over TCP and over UDP; what does the receiver see? */
// capture: with=net.c
#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

#include "net.h"

static const char *parts[] = {"ab", "cd", "efgh"};

static void over_tcp(void)
{
    int lfd = tcp_listen(44162);
    if (fork() == 0) {
        int fd = tcp_connect(44162);
        for (int i = 0; i < 3; i++)
            send(fd, parts[i], strlen(parts[i]), 0);
        close(fd);
        _exit(0);
    }
    int c = accept(lfd, NULL, NULL);
    wait(NULL);                                  /* the sender has finished */
    char buf[64];
    ssize_t n;
    while ((n = recv(c, buf, sizeof buf, 0)) > 0)
        printf("TCP: recv returned %zd bytes: %.*s\n", n, (int)n, buf);
    close(c);
    close(lfd);
}

static void over_udp(void)
{
    int fd = socket(AF_INET, SOCK_DGRAM, 0);     /* a datagram socket */
    struct sockaddr_in me = {0};
    me.sin_family = AF_INET;
    me.sin_port = htons(44163);
    me.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    bind(fd, (struct sockaddr *)&me, sizeof me);
    if (fork() == 0) {
        int out = socket(AF_INET, SOCK_DGRAM, 0);
        for (int i = 0; i < 3; i++)               /* no connection: each says where */
            sendto(out, parts[i], strlen(parts[i]), 0, (struct sockaddr *)&me, sizeof me);
        _exit(0);
    }
    wait(NULL);
    char buf[64];
    for (int i = 0; i < 3; i++) {
        ssize_t n = recvfrom(fd, buf, sizeof buf, 0, NULL, NULL);
        printf("UDP: recvfrom returned %zd bytes: %.*s\n", n, (int)n, buf);
    }
    close(fd);
}

int main(void)
{
    over_tcp();
    over_udp();
    return 0;
}
