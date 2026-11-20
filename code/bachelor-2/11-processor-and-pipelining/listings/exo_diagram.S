# exo_diagram.S: one load, used at once.
main:   lw   t0, 0(sp)
        addi t1, t0, 1
        addi t2, zero, 5
        add  t3, t1, t2
        ret
