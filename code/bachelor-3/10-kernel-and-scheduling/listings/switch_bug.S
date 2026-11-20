# switch_bug.S -- switch.S with a switch that forgets s1: the rest is unchanged.
        .data
ctx_main: .space 56             # a context: ra, sp, s0 .. s11, 14 words
ctx_a:  .space 56
ctx_b:  .space 56
        .align 4                # stacks aligned to 16 bytes, as the convention asks
        .space 1024
stack_a:                        # stacks grow down: the label is the top
        .space 1024
stack_b:
        .text
main:
        la   t0, ctx_a          # A starts at task_a, on its own stack
        la   t1, task_a
        sw   t1, 0(t0)
        la   t1, stack_a
        sw   t1, 4(t0)
        la   t0, ctx_b          # B likewise
        la   t1, task_b
        sw   t1, 0(t0)
        la   t1, stack_b
        sw   t1, 4(t0)
        la   a0, ctx_main
        la   a1, ctx_a
        call switch            # run A; we come back when someone switches to ctx_main
        li   a7, 10
        ecall

task_a: li   s1, 1              # A counts 1, 2, 3 in s1
loop_a: li   a0, 'A'
        call show
        la   a0, ctx_a
        la   a1, ctx_b
        call switch            # let B run
        addi s1, s1, 1
        li   t0, 4
        blt  s1, t0, loop_a
        la   a0, ctx_a
        la   a1, ctx_main
        call switch            # A is done: back to main, for good

task_b: li   s1, 10             # B counts 10, 20, 30 in its own s1
loop_b: li   a0, 'B'
        call show
        la   a0, ctx_b
        la   a1, ctx_a
        call switch
        addi s1, s1, 10
        j    loop_b

show:   li   a7, 11             # print the letter in a0, then s1, then a newline
        ecall
        mv   a0, s1
        li   a7, 1
        ecall
        li   a0, '\n'
        li   a7, 11
        ecall
        ret

# switch(a0 = where to save this context, a1 = the context to resume)
switch: sw   ra, 0(a0)
        sw   sp, 4(a0)
        sw   s0, 8(a0)
        sw   s2, 16(a0)
        sw   s3, 20(a0)
        sw   s4, 24(a0)
        sw   s5, 28(a0)
        sw   s6, 32(a0)
        sw   s7, 36(a0)
        sw   s8, 40(a0)
        sw   s9, 44(a0)
        sw   s10, 48(a0)
        sw   s11, 52(a0)
        lw   ra, 0(a1)
        lw   sp, 4(a1)
        lw   s0, 8(a1)
        lw   s2, 16(a1)
        lw   s3, 20(a1)
        lw   s4, 24(a1)
        lw   s5, 28(a1)
        lw   s6, 32(a1)
        lw   s7, 36(a1)
        lw   s8, 40(a1)
        lw   s9, 44(a1)
        lw   s10, 48(a1)
        lw   s11, 52(a1)
        ret                     # to the resumed context's ra: where it called switch
