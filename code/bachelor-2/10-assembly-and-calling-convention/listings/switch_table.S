# switch_table.S: the fine per day late by kind:
# switch (kind) { case 0: 10; case 1: 50; case 2: 5; case 3: 20; default: 0 }
        .data
kinds:  .word 1, 0, 3, 7, 2
table:  .word book, film, magazine, map     # the addresses of the four cases
        .text
main:   la   s0, kinds
        li   s1, 5
next:   lw   t0, 0(s0)
        li   t1, 4
        bgeu t0, t1, other      # bounds check: kind < 4, unsigned (a negative kind is huge)
        la   t1, table
        slli t0, t0, 2
        add  t1, t1, t0
        lw   t1, 0(t1)          # the address of the case
        jr   t1                 # one indirect jump, whatever the number of cases
book:   li   a0, 10
        j    done
film:   li   a0, 50
        j    done
magazine:
        li   a0, 5
        j    done
map:    li   a0, 20
        j    done
other:  li   a0, 0
done:   li   a7, 1
        ecall
        li   a0, ' '
        li   a7, 11
        ecall
        addi s0, s0, 4
        addi s1, s1, -1
        bnez s1, next
        li   a0, 0
        li   a7, 93
        ecall
