# capture: rv=asm
# constants.S: how li builds constants of every size.
        .text
main:   li   t0, 2047           # fits in 12 signed bits: one addi
        li   t1, -2048
        li   t2, 2048           # does not: lui, then addi
        li   t3, 0x12345678
        li   t4, 0x12345fff     # low 12 bits 0xfff = -1 when read signed: hi is rounded up
        li   t5, 0x7ffff000     # low 12 bits zero: lui alone
        li   t6, -1
        ret
