# memory.S: byte order, sign and zero extension, and a word built from bytes.
        .data
w:      .word 0x12345678
b:      .byte 0xff, 0x7f
        .text
main:   la   s0, w
        li   s1, 0
bytes:  add  t0, s0, s1
        lbu  a0, 0(t0)          # the bytes of w, from the lowest address up
        call print_hex
        addi s1, s1, 1
        li   t1, 4
        blt  s1, t1, bytes
        la   s0, b
        lb   a0, 0(s0)          # 0xff read signed: -1
        call print_dec
        lbu  a0, 0(s0)          # 0xff read unsigned: 255
        call print_dec
        lh   a0, 0(s0)          # the half 0x7fff (bytes ff 7f, little-endian): 32767
        call print_dec
        li   a0, 0
        li   a7, 93
        ecall
print_hex:                      # prints a0 (one byte) as two hex digits and a space
        srli t2, a0, 4
        andi t3, a0, 15
        li   a7, 11
        mv   a0, t2
        addi a0, a0, '0'
        li   t4, 10
        blt  t2, t4, d1
        addi a0, a0, 39         # 'a' - '0' - 10
d1:     ecall
        mv   a0, t3
        addi a0, a0, '0'
        blt  t3, t4, d2
        addi a0, a0, 39
d2:     ecall
        li   a0, ' '
        ecall
        ret
print_dec:                      # prints a0 in decimal and a space
        li   a7, 1
        ecall
        li   a0, ' '
        li   a7, 11
        ecall
        ret
