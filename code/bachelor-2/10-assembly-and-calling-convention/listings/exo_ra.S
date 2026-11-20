# capture: args=--steps 200 exit
# exo_ra.S: double(x) calls inc twice; the program never ends.
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        li   a0, 20
        call double_plus_two
        li   a7, 1
        ecall
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
double_plus_two:                # returns 2x + 2
        add  a0, a0, a0
        call inc
        call inc
        ret
inc:    addi a0, a0, 1
        ret
