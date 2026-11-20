# fib.S: naive recursive fib(n) under the convention, n read from input (exercise 11).
        .text
fib:    li   t0, 2
        blt  a0, t0, base       # fib(0) = 0, fib(1) = 1
        addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s0, 8(sp)
        sw   s1, 4(sp)
        mv   s0, a0
        addi a0, a0, -1
        call fib
        mv   s1, a0             # fib(n - 1)
        addi a0, s0, -2
        call fib
        add  a0, s1, a0
        lw   s1, 4(sp)
        lw   s0, 8(sp)
        lw   ra, 12(sp)
        addi sp, sp, 16
base:   ret
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        li   a7, 5
        ecall
        call fib
        li   a7, 1
        ecall
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
