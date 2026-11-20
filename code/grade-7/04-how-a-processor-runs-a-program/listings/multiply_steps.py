from toymachine import Machine, assemble

code = assemble(open("multiply.toy").read())
for b in range(1, 11):
    machine = Machine(code, inputs=[6, b])
    machine.run()
    print(f"6 x {b:2} = {machine.outputs[0]:3}   steps: {machine.steps}")
