# four.S: add, sw, lw and beq, the four instructions traced through the datapath.
main:   addi sp, sp, -16
        addi t0, zero, 7
        addi t1, zero, 5
        add  t2, t0, t1         # 12
        sw   t2, 12(sp)         # to memory
        lw   t3, 12(sp)         # and back
        beq  t2, t3, same       # equal: taken
        addi a0, zero, 1
same:   addi a0, zero, 0
        addi sp, sp, 16
        ret
