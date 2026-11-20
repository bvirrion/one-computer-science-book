/* net.h: the chapter's small socket library (loopback only). */
#ifndef NET_H
#define NET_H

#include <stddef.h>
#include <stdint.h>
#include <sys/types.h>

int tcp_listen(int port);                        /* listening socket on 127.0.0.1:port */
int tcp_connect(int port);                       /* connected socket to 127.0.0.1:port */
int send_all(int fd, const void *buf, size_t n); /* 0, or -1 on error */
ssize_t recv_all(int fd, void *buf, size_t n);   /* n, fewer at end of stream, -1 */
size_t frame(char *out, const char *msg, uint32_t n);         /* 4 + n bytes */
size_t unframe(const char *in, size_t len, const char **msg, uint32_t *n);
int send_msg(int fd, const char *msg, uint32_t n);
ssize_t recv_msg(int fd, char *buf, size_t cap); /* length; -1 at end or too long */

#endif
