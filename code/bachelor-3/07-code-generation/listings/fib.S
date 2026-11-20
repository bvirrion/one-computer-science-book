.data
.text
fib:
    addi sp, sp, -32
    sw ra, 28(sp)
    sw a0, 0(sp)
    lw t0, 0(sp)
    li t1, 2
    blt t0, t1, .Lfib_1
    j .Lfib_2
.Lfib_1:
    lw a0, 0(sp)
    j .Lfib_ret
    j .Lfib_3
.Lfib_2:
.Lfib_3:
    lw t0, 0(sp)
    addi t0, t0, -1
    sw t0, 4(sp)
    lw a0, 4(sp)
    call fib
    sw a0, 8(sp)
    lw t0, 0(sp)
    addi t0, t0, -2
    sw t0, 12(sp)
    lw a0, 12(sp)
    call fib
    sw a0, 16(sp)
    lw t0, 8(sp)
    lw t1, 16(sp)
    add t0, t0, t1
    sw t0, 20(sp)
    lw a0, 20(sp)
    j .Lfib_ret
    li a0, 0
    j .Lfib_ret
.Lfib_ret:
    lw ra, 28(sp)
    addi sp, sp, 32
    ret
main:
    addi sp, sp, -16
    sw ra, 12(sp)
    li a7, 5
    ecall
    sw a0, 0(sp)
    lw t0, 0(sp)
    sw t0, 4(sp)
    lw a0, 4(sp)
    call fib
    sw a0, 8(sp)
    lw a0, 8(sp)
    li a7, 1
    ecall
    li a0, 10
    li a7, 11
    ecall
    li a0, 0
    j .Lmain_ret
    li a0, 0
    j .Lmain_ret
.Lmain_ret:
    lw ra, 12(sp)
    addi sp, sp, 16
    ret
