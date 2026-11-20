# capture: rv=asm args=--fields
# exo_encode.S: encode these three by hand, then check.
main:   addi a0, a0, -1
        sw   ra, 12(sp)
        beq  a0, zero, main
