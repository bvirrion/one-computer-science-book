# strlen.S: the length of a NUL-terminated string, byte by byte.
        .data
s:      .asciz "Quay Street"
        .text
main:   la   t0, s
        mv   t1, t0             # start
next:   lbu  t2, 0(t0)
        beqz t2, end            # the NUL byte ends the string
        addi t0, t0, 1
        j    next
end:    sub  a0, t0, t1         # length = end - start
        li   a7, 1
        ecall
        li   a0, 0
        ret
