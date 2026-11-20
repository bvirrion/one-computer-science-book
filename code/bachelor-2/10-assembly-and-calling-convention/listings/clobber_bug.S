# clobber_bug.S: main keeps a running total in s0; fine() uses s0 too, without saving it.
        .data
days:   .word 30, 10, 25
        .text
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        la   s1, days
        li   s0, 0              # total, in a callee-saved register: should survive calls
        li   s2, 3
loop:   lw   a0, 0(s1)
        call fine
        add  s0, s0, a0
        addi s1, s1, 4
        addi s2, s2, -1
        bnez s2, loop
        mv   a0, s0
        li   a7, 1
        ecall                   # expected: 90 + 0 + 40 = 130
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret

fine:   li   s0, 21             # BUG: s0 is callee-saved, and fine() does not save it
        sub  a0, a0, s0         # days late
        bgtz a0, late
        li   a0, 0
        ret
late:   li   t0, 10
        mul  a0, a0, t0         # 10 cents a day
        ret
