# two_loops.S -- two programs that never give the processor up: each prints its letter
# 12 times, with a delay loop between letters, then exits.
        .text
task_a: li   s1, 12
next_a: li   a0, 'a'
        li   a7, 11
        ecall
        li   t0, 8              # a delay: 8 turns of an empty loop
wait_a: addi t0, t0, -1
        bnez t0, wait_a
        addi s1, s1, -1
        bnez s1, next_a
        li   a7, 10
        ecall

task_b: li   s1, 12
next_b: li   a0, 'b'
        li   a7, 11
        ecall
        li   t0, 8
wait_b: addi t0, t0, -1
        bnez t0, wait_b
        addi s1, s1, -1
        bnez s1, next_b
        li   a7, 10
        ecall
