# first.S: the sum 1 + 2 + ... + n, for n = 100, printed with ecall.
        .text
main:   li   t0, 100            # n
        li   a0, 0              # sum = 0
        li   t1, 1              # k = 1
loop:   add  a0, a0, t1         # sum = sum + k
        addi t1, t1, 1          # k = k + 1
        bge  t0, t1, loop       # while n >= k
        li   a7, 1              # print int: the number in a7, the argument in a0
        ecall
        li   a0, '\n'
        li   a7, 11             # print char
        ecall
        li   a0, 0              # exit status 0
        ret
