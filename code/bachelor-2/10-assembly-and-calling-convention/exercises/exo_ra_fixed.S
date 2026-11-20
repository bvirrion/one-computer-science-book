# exo_ra_fixed.S: exercise 6 fixed: double_plus_two saves and restores ra.
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
        addi sp, sp, -16
        sw   ra, 12(sp)         # it calls: save its return address
        add  a0, a0, a0
        call inc
        call inc
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret
inc:    addi a0, a0, 1
        ret
