from lift import safe, step

state = (0, "closed", "stop", None)
print("Commands: call0 call1 call2 open close arrive quit")
while True:
    command = input("lift> ").strip()
    if command == "quit":
        break
    if command not in {"call0", "call1", "call2", "open", "close", "arrive"}:
        print("  unknown command:", command)
        continue
    state = step(state, command)
    floor, door, motor, target = state
    print(f"  floor {floor}, door {door}, motor {motor}, going to {target}")
    assert safe(state)
