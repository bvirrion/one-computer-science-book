/* fib.c -- the same function in C, for gcc to compile to x86-64 */
int fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
