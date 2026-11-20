# independent.S: five instructions, none using the result of another.
main:   addi t0, zero, 1
        addi t1, zero, 2
        addi t2, zero, 3
        addi a0, zero, 0
        ret
