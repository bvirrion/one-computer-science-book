# capture: args=--trace
# hook.S: x = a[i] + 1, with the address of a in a0, i in a1, and x in a2.
        .data
a:      .word 65, 133, 412, 98
        .text
main:   la   a0, a              # the address of the array
        li   a1, 2              # i = 2
        slli t0, a1, 2          # i * 4: an int is 4 bytes
        add  t0, a0, t0         # the address of a[i]
        lw   t1, 0(t0)          # load a[i] from memory into a register
        addi a2, t1, 1          # a[i] + 1, in a register
        mv   a0, a2
        li   a7, 1              # print it
        ecall
        li   a0, 0
        ret
