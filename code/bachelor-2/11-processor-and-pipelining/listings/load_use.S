# load_use.S: five instructions, two of them using a value loaded just before.
        .data
v:      .word 20, 22, 0
        .text
main:   la   a0, v
        lw   t0, 0(a0)
        add  t1, t0, t0         # needs t0 from the load: load-use
        lw   t2, 4(a0)
        add  t3, t1, t2         # needs t2 from the load: load-use
        sw   t3, 8(a0)          # needs t3 from the add: forwarded, no stall
        li   a0, 0
        ret
