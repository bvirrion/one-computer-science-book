"""A toy-machine program kept in a Python string: data until the simulator runs it."""
from toymachine import Machine, assemble

COUNTDOWN = """
        LOADI R0, 3
        LOADI R1, 1
loop:   OUT   R0
        SUB   R0, R1
        JNZ   loop
        HALT
"""
code = assemble(COUNTDOWN)                       # 256 bytes of memory
print("the first ten bytes:", code[:10])
m = Machine(code)
m.run()
print("outputs:", m.outputs, " steps:", m.steps)
code[1] = 5                                      # change one byte of the program
m = Machine(code)
m.run()
print("after changing byte 1 to 5:", m.outputs, " steps:", m.steps)
