/* echo_pair.c: a TCP server and its client, in two processes on one machine. */
#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

#define PORT 44160

static void client(void)
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);              /* 1. a socket */
    struct sockaddr_in srv = {0};
    srv.sin_family = AF_INET;
    srv.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &srv.sin_addr);
    connect(fd, (struct sockaddr *)&srv, sizeof srv);      /* 2. to the server */
    send(fd, "hello, server", 13, 0);
    char buf[64];
    ssize_t n = recv(fd, buf, sizeof buf, 0);
    printf("client: received %zd bytes: %.*s\n", n, (int)n, buf);
    close(fd);
}

static void server(int lfd)
{
    struct sockaddr_in peer;
    socklen_t len = sizeof peer;
    int c = accept(lfd, (struct sockaddr *)&peer, &len);   /* 4. one connection */
    char buf[64];
    ssize_t n = recv(c, buf, sizeof buf, 0);
    printf("server: a client on %s sent %zd bytes\n", inet_ntoa(peer.sin_addr), n);
    fflush(stdout);
    send(c, buf, n, 0);                                    /* echo them back */
    close(c);
}

int main(void)
{
    int lfd = socket(AF_INET, SOCK_STREAM, 0);             /* 1. a socket */
    int one = 1;
    setsockopt(lfd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    struct sockaddr_in me = {0};
    me.sin_family = AF_INET;
    me.sin_port = htons(PORT);
    me.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(lfd, (struct sockaddr *)&me, sizeof me) != 0) {  /* 2. an address */
        perror("bind");
        return 1;
    }
    listen(lfd, 16);                                       /* 3. accept connections */
    if (fork() == 0) {
        close(lfd);
        client();
        exit(0);                                           /* flushes stdout */
    }
    server(lfd);
    wait(NULL);
    close(lfd);
    return 0;
}
