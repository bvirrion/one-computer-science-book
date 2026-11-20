# exo_x0.S: an instruction that writes x0, then one that reads it.
main:   addi t0, zero, 41
        addi zero, t0, 1        # a no-op: x0 keeps 0
        add  a0, zero, zero     # a0 = 0
        ret
