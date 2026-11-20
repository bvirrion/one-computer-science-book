# max.S: the largest element of a non-empty array of signed words (exercise 3).
# max(a0 = address, a1 = n >= 1) -> a0
        .text
main:   la   a0, temps
        li   a1, 6
        call max
        li   a7, 1
        ecall
        li   a0, 0
        li   a7, 93
        ecall
max:    lw   t0, 0(a0)          # best = a[0]
        slli a1, a1, 2
        add  a1, a0, a1         # end
next:   addi a0, a0, 4
        bgeu a0, a1, done
        lw   t1, 0(a0)
        bge  t0, t1, next       # signed comparison: keep best if best >= a[i]
        mv   t0, t1
        j    next
done:   mv   a0, t0
        ret
        .data
temps:  .word -12, 4, -3, 19, 7, -40
