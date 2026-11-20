from toymachine import Machine, assemble

code = assemble(open("multiply.toy").read())
for a, b in [(3, 50), (50, 3), (7, 30), (30, 7), (7, 200)]:
    machine = Machine(code, inputs=[a, b])
    machine.run()
    print(f"{a} x {b} = {machine.outputs[0]}   steps: {machine.steps}")
