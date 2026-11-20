# capture: exit
# misaligned.S: a word load from an address that is not a multiple of 4.
        .data
pages:  .word 65, 133
        .text
main:   la   t0, pages
        lw   a0, 2(t0)          # bytes 2 to 5: across two words
        li   a7, 1
        ecall
        ret
