# switch2.S: a jump table for cases 3 to 7, with its bounds check (exercise 12).
# switch (shelf) { case 3: 'A'; case 4: 'B'; case 5: 'B'; case 7: 'D'; default: '?' }
        .text
main:   la   s0, shelves
        li   s1, 7
loop:   lw   t0, 0(s0)
        addi t0, t0, -3         # case 3 becomes index 0
        li   t1, 5
        bgeu t0, t1, other      # one unsigned test: below 3 wraps to a huge number
        la   t1, table
        slli t0, t0, 2
        add  t1, t1, t0
        lw   t1, 0(t1)
        jr   t1
ca:     li   a0, 'A'
        j    print
cb:     li   a0, 'B'
        j    print
cd:     li   a0, 'D'
        j    print
other:  li   a0, '?'
print:  li   a7, 11
        ecall
        addi s0, s0, 4
        addi s1, s1, -1
        bnez s1, loop
        li   a0, 0
        li   a7, 93
        ecall
        .data
table:  .word ca, cb, cb, other, cd      # case 6 is a gap: it goes to default
shelves: .word 3, 4, 5, 6, 7, 2, 8
