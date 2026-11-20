# count.S: the check digit of a book code read as a decimal number.
# Digits from the right, position i = 0, 1, 2, ...: weight 3 at even positions, 1 at odd ones;
# check = (10 - (weighted sum mod 10)) mod 10.
        .text
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s0, 8(sp)
        sw   s1, 4(sp)
        sw   s2, 0(sp)
        li   a7, 5
        ecall                   # a0 = the code
        mv   s0, a0             # the digits still to read
        li   s1, 0              # i
        li   s2, 0              # the weighted sum
digit:  li   t0, 10
        remu a0, s0, t0         # the last digit
        divu s0, s0, t0         # drop it
        mv   a1, s1
        call weigh              # a0 = weight(i) * digit
        add  s2, s2, a0
        addi s1, s1, 1
        bnez s0, digit          # a code has at least one digit: the test at the bottom
        li   t0, 10
        remu t1, s2, t0
        sub  t1, t0, t1
        remu a0, t1, t0         # (10 - sum mod 10) mod 10
        li   a7, 1
        ecall
        li   a0, '\n'
        li   a7, 11
        ecall
        lw   s2, 0(sp)
        lw   s1, 4(sp)
        lw   s0, 8(sp)
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret

weigh:                          # a leaf: a0 = digit, a1 = position -> weighted digit
        andi t0, a1, 1          # 0 at even positions, 1 at odd ones
        slli t0, t0, 1          # 0 or 2
        li   t1, 3
        sub  t1, t1, t0         # weight 3 or 1, without a branch
        mul  a0, a0, t1
        ret
