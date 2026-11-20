/* hello_write.c: one line through the C library, one straight to the kernel. */
#include <stdio.h>
#include <unistd.h>

int main(void)
{
    printf("hello, library\n");             /* a library call: kept in a buffer for now */
    ssize_t n = write(1, "hello, kernel\n", 14);   /* a system call: descriptor 1, 14 bytes */
    return n == 14 ? 0 : 1;                 /* returning from main flushes the buffer */
}
