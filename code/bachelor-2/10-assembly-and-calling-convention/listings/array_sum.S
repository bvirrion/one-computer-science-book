# array_sum.S: the sum of an array of words, walked with a pointer.
        .data
pages:  .word 65, 133, 412, 98, 251, 320
n:      .word 6
        .text
main:   la   t0, pages          # p = &pages[0]
        la   t1, n
        lw   t1, 0(t1)          # n
        slli t1, t1, 2
        add  t1, t0, t1         # end = p + 4n: one past the last element
        li   a0, 0
loop:   bgeu t0, t1, done       # while p < end (addresses compare unsigned)
        lw   t2, 0(t0)
        add  a0, a0, t2
        addi t0, t0, 4          # p++ moves 4 bytes
        j    loop
done:   li   a7, 1
        ecall
        li   a0, 0
        ret
