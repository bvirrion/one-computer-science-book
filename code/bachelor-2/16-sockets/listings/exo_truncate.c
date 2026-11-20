/* exo_truncate.c: a datagram of 100 bytes, a buffer of 10 (exercise 5). */
#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void)
{
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in me = {0};
    me.sin_family = AF_INET;
    me.sin_port = htons(44165);
    me.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    bind(fd, (struct sockaddr *)&me, sizeof me);
    char big[100];
    memset(big, 'x', sizeof big);
    sendto(fd, big, sizeof big, 0, (struct sockaddr *)&me, sizeof me);   /* to itself */
    sendto(fd, "next", 4, 0, (struct sockaddr *)&me, sizeof me);
    char buf[10];
    ssize_t n = recvfrom(fd, buf, sizeof buf, 0, NULL, NULL);
    printf("first recvfrom: %zd bytes\n", n);
    n = recvfrom(fd, buf, sizeof buf, 0, NULL, NULL);
    printf("second recvfrom: %zd bytes: %.*s\n", n, (int)n, buf);
    return 0;
}
