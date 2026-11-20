# forwarding.S: each instruction uses the results of the ones just before it.
main:   addi a1, zero, 7
        addi a2, zero, 5
        add  t0, a1, a2
        sub  t1, t0, a2         # t0 from the instruction just ahead
        and  t2, t0, t1         # t0 from two ahead, t1 from one ahead
        or   t3, t0, t2         # t0 from three ahead: already in the register file
        ret
