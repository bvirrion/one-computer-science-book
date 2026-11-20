# loan_fine.S: hand-compiled (exercise 9)
#   struct loan { int days; short rate; char lost; };      offsets 0, 4, 6; size 8
#   int fine(const struct loan *l) { if (l->lost) return 2000; int d = l->days - 21;
#                                    return d > 0 ? d * l->rate : 0; }
        .text
fine:   lbu  t0, 6(a0)          # l->lost
        bnez t0, lost
        lw   t1, 0(a0)          # l->days
        addi t1, t1, -21
        blez t1, none
        lh   t2, 4(a0)          # l->rate, a signed short
        mul  a0, t1, t2
        ret
lost:   li   a0, 2000
        ret
none:   li   a0, 0
        ret
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s0, 8(sp)
        sw   s1, 4(sp)
        la   s0, loans
        li   s1, 3
again:  mv   a0, s0
        call fine
        li   a7, 1
        ecall
        li   a0, ' '
        li   a7, 11
        ecall
        addi s0, s0, 8
        addi s1, s1, -1
        bnez s1, again
        lw   s1, 4(sp)
        lw   s0, 8(sp)
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
        .data
loans:  .word 30
        .half 10
        .byte 0, 0
        .word 12
        .half 10
        .byte 0, 0
        .word 5
        .half 25
        .byte 1, 0
