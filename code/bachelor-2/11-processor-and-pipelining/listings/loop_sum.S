# loop_sum.S: the sum of 32 page counts; each element is used just after it is loaded.
        .data
pages:  .word 65, 133, 412, 98, 251, 320, 189, 77, 501, 12, 260, 145, 38, 199, 87, 300
        .word 154, 222, 96, 410, 73, 288, 167, 345, 59, 230, 118, 402, 61, 276, 190, 133
        .text
main:   la   t0, pages
        addi t1, t0, 128        # end: 32 words
        li   a0, 0
loop:   lw   t2, 0(t0)
        add  a0, a0, t2         # uses t2 in the very next instruction: a load-use hazard
        addi t0, t0, 4
        bltu t0, t1, loop
        li   a7, 1
        ecall
        li   a0, 0
        ret
