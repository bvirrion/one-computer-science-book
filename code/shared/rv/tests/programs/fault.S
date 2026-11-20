main:   li   a0, 7
        li   a7, 1
        ecall               # prints 7, no newline
        li   a1, 0
loop:   lw   a0, 0(a1)      # reads address 0
        ret
