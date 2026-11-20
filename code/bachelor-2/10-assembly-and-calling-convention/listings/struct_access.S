# struct_access.S: struct book { int pages; short year; char shelf; }, 8 bytes; three of them.
# The total of the pages of the books on shelf 'B'.
        .data
books:  .word 65                # books[0].pages   offset 0
        .half 2002              #          .year   offset 4
        .byte 'B', 0            #          .shelf  offset 6, then one byte of padding
        .word 133
        .half 1996
        .byte 'A', 0
        .word 412
        .half 2011
        .byte 'B', 0
        .text
main:   la   t0, books
        li   t1, 3              # count
        li   t3, 'B'
        li   a0, 0
loop:   lbu  t2, 6(t0)          # books[i].shelf: base + 6
        bne  t2, t3, skip
        lw   t2, 0(t0)          # books[i].pages: base + 0
        add  a0, a0, t2
skip:   addi t0, t0, 8          # the next book: 8 bytes further
        addi t1, t1, -1
        bnez t1, loop
        li   a7, 1
        ecall
        li   a0, 0
        ret
