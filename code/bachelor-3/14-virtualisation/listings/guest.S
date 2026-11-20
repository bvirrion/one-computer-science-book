# guest.S -- a tiny guest kernel. It drives three devices through control registers (CSRs):
# a console at 0x5c0, a number display at 0x5c3 and a power switch at 0x5c1, and reads a
# clock at 0x5c2. This machine has no CSR instructions, so they are written as raw words.
# capture: exit
        .data
msg:    .asciz "hello from the guest\n"
        .text
main:
        la    t0, msg
print:  lbu   a0, 0(t0)
        beqz  a0, sum
        .word 0x5c051073        # csrw 0x5c0, a0: send one character to the console
        addi  t0, t0, 1
        j     print
sum:    li    a0, 0             # some ordinary work: 1 + 2 + ... + 100
        li    t1, 100
add:    add   a0, a0, t1
        addi  t1, t1, -1
        bnez  t1, add
        .word 0x5c351073        # csrw 0x5c3, a0: show the sum
        .word 0x5c202573        # csrr a0, 0x5c2: read the clock
        .word 0x5c351073        # csrw 0x5c3, a0: show it
        li    a0, 0
        .word 0x5c151073        # csrw 0x5c1, a0: power off, status 0
