# collatz.S: the total number of 3n + 1 steps from every start 1 to 30.
        .text
main:   li   s0, 1              # start
        li   a0, 0              # total steps
        li   t2, 1
        li   t3, 30
next:   mv   t0, s0
walk:   beq  t0, t2, end
        andi t1, t0, 1
        bnez t1, odd
        srli t0, t0, 1
        j    count
odd:    slli t1, t0, 1
        add  t0, t0, t1
        addi t0, t0, 1
count:  addi a0, a0, 1
        j    walk
end:    addi s0, s0, 1
        bge  t3, s0, next
        li   a7, 1
        ecall
        li   a0, 0
        ret
