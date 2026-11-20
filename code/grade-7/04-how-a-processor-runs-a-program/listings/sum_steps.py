from toymachine import Machine, assemble

code = assemble(open("sum.toy").read())
for n in range(1, 11):
    machine = Machine(code, inputs=[n])
    machine.run()
    print(f"n = {n:2}   total = {machine.outputs[0]:2}   steps: {machine.steps}")
