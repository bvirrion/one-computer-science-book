"""monitor_sim.py -- a monitor run step by step by a script, with Hoare or Mesa
semantics, and a consumer that tests its condition with `if` or with `while`."""


def consumer(buf, use_while):
    if use_while:
        while not buf:
            yield "wait"  # releases the monitor; resumes holding it
    elif not buf:
        yield "wait"
    return f"takes {buf.pop(0)}" if buf else "takes from an empty buffer!"


def producer(buf):
    buf.append("item")
    yield "signal"  # wake one waiting consumer
    return "leaves"


def run(script, hoare, use_while):
    buf, waiting, done, log = [], [], set(), []
    threads = {"C1": consumer(buf, use_while), "C2": consumer(buf, use_while),
               "P": producer(buf)}

    def resume(name):  # run a thread until it waits or leaves the monitor
        try:
            event = next(threads[name])
        except StopIteration as end:
            log.append(f"{name} {end.value}")
            done.add(name)
            return
        if event == "signal":
            log.append(f"{name} puts an item and signals")
        if event == "wait":
            log.append(f"{name} waits")
            waiting.append(name)
        elif event == "signal" and waiting:
            woken = waiting.pop(0)
            if hoare:  # Hoare: the waiter runs at once, the condition still true
                resume(woken)
            # Mesa: the waiter only leaves the waiting list; it runs when scheduled
        if event == "signal":
            resume(name)

    for name in script:
        if name.startswith("~"):  # a spurious wake-up: out of the list, no signal
            waiting.remove(name[1:])
        elif name not in waiting and name not in done:  # awake and unfinished: run
            resume(name)
    return log


if __name__ == "__main__":
    SCRIPT = ["C1", "P", "C2", "C1"]  # C1 waits; P signals; C2 enters first; then C1
    for hoare in (True, False):
        for use_while in (False, True):
            log = run(SCRIPT, hoare, use_while)
            test = "while" if use_while else "if"
            kind = f"{'Hoare' if hoare else 'Mesa':<5} {test:<5}"
            print(f"{kind} | {', '.join(log)}")
