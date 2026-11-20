# strcmp.S: strcmp(a0, a1) -> a0 < 0, 0 or > 0, comparing unsigned bytes (exercise 7). A leaf.
        .text
strcmp: lbu  t0, 0(a0)
        lbu  t1, 0(a1)
        bne  t0, t1, diff
        beqz t0, diff           # both ended: equal (t0 - t1 = 0)
        addi a0, a0, 1
        addi a1, a1, 1
        j    strcmp
diff:   sub  a0, t0, t1
        ret
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        la   a0, str1
        la   a1, str2
        call strcmp             # "Mill Lane" vs "Mill Row": 'L' < 'R'
        call sign
        la   a0, str2
        la   a1, str2
        call strcmp
        call sign
        la   a0, str3
        la   a1, str1
        call strcmp             # "Mill" vs "Mill Lane": the shorter is smaller
        call sign
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
sign:   slt  t0, zero, a0       # prints -1, 0 or 1 and a space
        slt  t1, a0, zero
        sub  a0, t0, t1
        li   a7, 1
        ecall
        li   a0, ' '
        li   a7, 11
        ecall
        ret
        .data
str1:   .asciz "Mill Lane"
str2:   .asciz "Mill Row"
str3:   .asciz "Mill"
