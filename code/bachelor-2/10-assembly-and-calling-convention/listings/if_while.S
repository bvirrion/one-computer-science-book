# if_while.S: if (x < 0) x = -x;  and  while (n != 1) { n = n even ? n/2 : 3n+1; steps++; }
        .text
main:   li   a0, -42            # x
        bgez a0, pos            # the condition reversed: skip the then-part when x >= 0
        neg  a0, a0             # x = -x
pos:    li   a7, 1
        ecall                   # prints 42
        li   a0, ' '
        li   a7, 11
        ecall
        li   t0, 27             # n
        li   a0, 0              # steps
        li   t2, 1
test:   beq  t0, t2, out        # while (n != 1): the test at the top
        andi t1, t0, 1
        bnez t1, odd
        srli t0, t0, 1          # n / 2
        j    step
odd:    slli t1, t0, 1
        add  t0, t0, t1         # 3n
        addi t0, t0, 1          # 3n + 1
step:   addi a0, a0, 1
        j    test
out:    li   a7, 1
        ecall                   # prints 111
        li   a0, 0
        ret
