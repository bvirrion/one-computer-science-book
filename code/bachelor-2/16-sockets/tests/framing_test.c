// test-with: ../listings/net.c ../exercises/linereader.c ../exercises/count_server.c ../exercises/chat.c
/* framing_test.c: framing round trips, partial frames, recv_all and the line reader on
   1-byte sends, the counting server and the chat server on port 44164. */
#define _POSIX_C_SOURCE 200809L
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#include "../exercises/linereader.h"
#include "net.h"

long count_serve(int lfd, int clients);
void chat_serve(int lfd, int total);

static void framing(void)
{
    static char wire[200000], msg[300][300];
    uint32_t len[300];
    size_t at = 0;
    srand(7);
    for (int i = 0; i < 300; i++) {             /* random messages, some empty, any bytes */
        len[i] = rand() % 300;
        for (uint32_t k = 0; k < len[i]; k++)
            msg[i][k] = (char)(rand() % 256);
        at += frame(wire + at, msg[i], len[i]);
    }
    size_t pos = 0;
    for (int i = 0; i < 300; i++) {
        const char *m;
        uint32_t n;
        assert(unframe(wire + pos, 3, &m, &n) == 0);              /* a cut length */
        assert(len[i] == 0 || unframe(wire + pos, 3 + len[i], &m, &n) == 0);
        size_t used = unframe(wire + pos, at - pos, &m, &n);
        assert(used == 4 + len[i] && n == len[i] && memcmp(m, msg[i], n) == 0);
        pos += used;
    }
    assert(pos == at);
}

static void trickle(void)                        /* the peer sends one byte at a time */
{
    int sv[2];
    socketpair(AF_UNIX, SOCK_STREAM, 0, sv);
    if (fork() == 0) {
        close(sv[0]);
        char buf[64];
        size_t n = frame(buf, "abcdef", 6);
        const char *text = "one\ntwo\n\nthree";
        for (size_t i = 0; i < n; i++)
            send(sv[1], buf + i, 1, 0);
        for (size_t i = 0; i < strlen(text); i++)
            send(sv[1], text + i, 1, 0);
        _exit(0);
    }
    close(sv[1]);
    char buf[64];
    assert(recv_msg(sv[0], buf, sizeof buf) == 6 && memcmp(buf, "abcdef", 6) == 0);
    struct linereader r;
    lr_init(&r, sv[0]);
    assert(lr_line(&r, buf, sizeof buf) == 3 && strcmp(buf, "one") == 0);
    assert(lr_line(&r, buf, sizeof buf) == 3 && strcmp(buf, "two") == 0);
    assert(lr_line(&r, buf, sizeof buf) == 0);
    assert(lr_line(&r, buf, sizeof buf) == -1);  /* "three" has no newline */
    wait(NULL);
    close(sv[0]);
}

static void counting(void)
{
    int lfd = tcp_listen(44164);
    if (fork() == 0) {
        for (int c = 0; c < 4; c++)
            if (fork() == 0) {                  /* 4 clients, 50 lines each */
                int fd = tcp_connect(44164);
                struct linereader r;
                lr_init(&r, fd);
                char line[32];
                for (int k = 0; k < 50; k++) {
                    send_all(fd, "x\n", 2);
                    assert(lr_line(&r, line, sizeof line) > 0 && atol(line) <= 200);
                }
                close(fd);
                _exit(0);
            }
        while (wait(NULL) > 0)
            ;
        _exit(0);
    }
    assert(count_serve(lfd, 4) == 200);
    wait(NULL);
    close(lfd);
}

static void chatting(void)
{
    int lfd = tcp_listen(44164);
    if (fork() == 0) {
        int a = tcp_connect(44164), b = tcp_connect(44164), c = tcp_connect(44164);
        nanosleep(&(struct timespec){0, 100000000L}, NULL);   /* all three accepted */
        send_all(a, "hi from a\n", 10);
        struct linereader rb, rc;
        lr_init(&rb, b);
        lr_init(&rc, c);
        char line[64];
        assert(lr_line(&rb, line, sizeof line) >= 0 && strcmp(line, "hi from a") == 0);
        assert(lr_line(&rc, line, sizeof line) >= 0 && strcmp(line, "hi from a") == 0);
        send_all(c, "and c\n", 6);
        struct linereader ra;
        lr_init(&ra, a);
        assert(lr_line(&ra, line, sizeof line) >= 0 && strcmp(line, "and c") == 0);
        assert(lr_line(&rb, line, sizeof line) >= 0 && strcmp(line, "and c") == 0);
        close(a), close(b), close(c);
        _exit(0);
    }
    chat_serve(lfd, 3);
    int s;
    wait(&s);
    assert(WIFEXITED(s) && WEXITSTATUS(s) == 0);
    close(lfd);
}

int main(void)
{
    framing();
    trickle();
    counting();
    chatting();
    printf("framing_test: all passed\n");
    return 0;
}
