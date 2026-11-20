# exo_bge.S: meant to print 1 + 2 + ... + 10 = 55.
main:   li   t0, 10             # n
        li   t1, 1              # k
        li   a0, 0
loop:   add  a0, a0, t1
        addi t1, t1, 1
        bge  t1, t0, loop       # "while k <= n"?
        li   a7, 1
        ecall
        li   a0, 0
        ret
