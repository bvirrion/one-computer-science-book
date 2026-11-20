"""Three toy programs without input, used by the listings of the chapter."""

COUNTDOWN = """
        LOADI R0, 3
        LOADI R1, 1
loop:   OUT   R0
        SUB   R0, R1
        JNZ   loop
        HALT
"""
FOREVER = """
loop:   JMP   loop
"""
WRAP = """
loop:   ADDI  R0, 1      ; 1, 2, ..., 255, then 0 again
        JNZ   loop
        HALT
"""
SPIN = """
loop:   ADDI  R0, 1      ; counts for ever, round and round
        JMP   loop
"""
