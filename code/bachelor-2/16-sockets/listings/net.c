/* net.c: sockets on the loopback address, complete sends and receives, framing. */
#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "net.h"

static struct sockaddr_in loopback(int port)
{
    struct sockaddr_in a;
    memset(&a, 0, sizeof a);
    a.sin_family = AF_INET;
    a.sin_port = htons(port);                    /* port in network byte order */
    a.sin_addr.s_addr = htonl(INADDR_LOOPBACK);  /* 127.0.0.1 */
    return a;
}

int tcp_listen(int port)
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    int one = 1;
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    struct sockaddr_in a = loopback(port);
    if (fd < 0 || bind(fd, (struct sockaddr *)&a, sizeof a) != 0 || listen(fd, 128) != 0)
        return -1;
    return fd;
}

int tcp_connect(int port)
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a = loopback(port);
    if (fd < 0 || connect(fd, (struct sockaddr *)&a, sizeof a) != 0) {
        if (fd >= 0)
            close(fd);
        return -1;
    }
    return fd;
}

int send_all(int fd, const void *buf, size_t n)
{
    const char *p = buf;
    while (n > 0) {
        ssize_t k = send(fd, p, n, MSG_NOSIGNAL); /* EPIPE instead of SIGPIPE */
        if (k <= 0)
            return -1;
        p += k, n -= k;
    }
    return 0;
}

ssize_t recv_all(int fd, void *buf, size_t n)
{
    size_t got = 0;
    while (got < n) {
        ssize_t k = recv(fd, (char *)buf + got, n - got, 0);
        if (k < 0)
            return -1;
        if (k == 0)
            break;                               /* end of stream */
        got += k;
    }
    return got;
}

size_t frame(char *out, const char *msg, uint32_t n)
{
    uint32_t len = htonl(n);                     /* the length, big-endian */
    memcpy(out, &len, 4);
    memcpy(out + 4, msg, n);
    return 4 + (size_t)n;
}

size_t unframe(const char *in, size_t len, const char **msg, uint32_t *n)
{
    if (len < 4)
        return 0;                                /* not even a whole length */
    uint32_t be;
    memcpy(&be, in, 4);
    *n = ntohl(be);
    if (len - 4 < *n)
        return 0;                                /* the message is not all there */
    *msg = in + 4;
    return 4 + (size_t)*n;
}

int send_msg(int fd, const char *msg, uint32_t n)
{
    uint32_t len = htonl(n);
    return send_all(fd, &len, 4) == 0 ? send_all(fd, msg, n) : -1;
}

ssize_t recv_msg(int fd, char *buf, size_t cap)
{
    uint32_t len;
    if (recv_all(fd, &len, 4) != 4)
        return -1;
    uint32_t n = ntohl(len);
    if (n > cap || recv_all(fd, buf, n) != (ssize_t)n)
        return -1;
    return n;
}
