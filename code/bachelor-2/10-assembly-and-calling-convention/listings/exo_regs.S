# capture: args=--regs
# exo_regs.S: six instructions. Predict a0, a1, a2, a3, a4 and a5.
main:   li   a0, -5
        srai a1, a0, 1
        srli a2, a0, 28
        slti a3, a0, 0
        sltiu a4, a0, 0
        xori a5, a0, -1
        li   a0, 0
        ret
