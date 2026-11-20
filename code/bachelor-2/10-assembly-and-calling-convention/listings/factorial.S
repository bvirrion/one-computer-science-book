# capture: args=--trace
# factorial.S: fact(n) = n * fact(n - 1), fact(0) = 1, under the calling convention; fact(3).
        .text
main:   addi sp, sp, -16
        sw   ra, 12(sp)         # main calls: it must keep its own return address
        li   a0, 3
        call fact
        li   a7, 1
        ecall                   # prints fact(3)
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret

fact:   addi sp, sp, -16        # prologue: a 16-byte frame
        sw   ra, 12(sp)         #   save the return address (fact calls fact)
        sw   s0, 8(sp)          #   save s0, callee-saved, before using it
        mv   s0, a0             # keep n across the call
        bnez a0, rec
        li   a0, 1              # fact(0) = 1
        j    epi
rec:    addi a0, a0, -1
        call fact               # a0 = fact(n - 1)
        mul  a0, s0, a0         # n * fact(n - 1)
epi:    lw   s0, 8(sp)          # epilogue: restore, pop, return
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret
