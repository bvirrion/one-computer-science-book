from assembler_m2 import assemble
from simulator_m3 import new_machine, run

COPY = """\
        LOAD  R0, [value]   ; R0 = 77
        STORE R0, [copy]
        LOAD  R1, [copy]
        OUT   R1
        HALT
value:  DATA  77
copy:   DATA  0
"""
m = new_machine(assemble(COPY))
print("outputs:", run(m), "| steps:", m["steps"], "| PC:", m["pc"])
print("memory 10 and 11:", m["mem"][10:12])
forever = new_machine(assemble("again: JMP again"))
try:
    run(forever, max_steps=500)
except RuntimeError as error:
    print("RuntimeError:", error)
