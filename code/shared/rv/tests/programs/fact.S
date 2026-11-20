# fact.S -- reads n, prints n! (recursive, with a stack frame per call)
        .data
eq:     .asciz "! = "
        .text
        .globl main
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s0, 8(sp)
        li   a7, 5              # read int -> a0
        ecall
        mv   s0, a0
        call fact
        mv   t0, a0
        mv   a0, s0
        li   a7, 1              # print int
        ecall
        la   a0, eq
        li   a7, 4              # print string
        ecall
        mv   a0, t0
        li   a7, 1
        ecall
        li   a0, '\n'
        li   a7, 11             # print char
        ecall
        lw   s0, 8(sp)
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
fact:   li   t1, 1
        ble  a0, t1, base       # 0! = 1! = 1
        addi sp, sp, -16
        sw   ra, 12(sp)
        sw   a0, 8(sp)
        addi a0, a0, -1
        call fact               # a0 = (n-1)!
        lw   t1, 8(sp)
        mul  a0, a0, t1
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret
base:   li   a0, 1
        ret
