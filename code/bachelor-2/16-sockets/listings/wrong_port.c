/* wrong_port.c: a server that forgets htons (exercise 2). */
#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void)
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in me = {0};
    me.sin_family = AF_INET;
    me.sin_port = 44164;                         /* meant: htons(44164) */
    me.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(fd, (struct sockaddr *)&me, sizeof me) != 0) {
        perror("bind");
        return 1;
    }
    listen(fd, 16);
    struct sockaddr_in got;
    socklen_t len = sizeof got;
    getsockname(fd, (struct sockaddr *)&got, &len);  /* where is it, really? */
    printf("asked for port 44164, listening on port %u\n", (unsigned)ntohs(got.sin_port));
    fflush(stdout);
    int c = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in to = me;
    to.sin_port = htons(44164);                  /* a client that does it right */
    if (connect(c, (struct sockaddr *)&to, sizeof to) != 0)
        perror("client: connect to 44164");
    return 0;
}
