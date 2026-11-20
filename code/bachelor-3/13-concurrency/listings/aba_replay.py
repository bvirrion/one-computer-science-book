"""aba_replay.py -- the ABA problem, replayed: two threads on a simulated Treiber stack,
interleaved by a script, first with a bare head pointer and then with a tagged one."""


class Stack:
    def __init__(self, names, tagged):
        self.next = {n: m for n, m in zip(names, names[1:] + [None])}
        self.head, self.tag, self.tagged = names[0], 0, tagged

    def read(self):  # what a thread reads before its compare-and-swap
        return (self.head, self.tag) if self.tagged else (self.head, None)

    def cas(self, expected, new_head):  # one atomic step
        if self.read() != expected:
            return False
        self.head, self.tag = new_head, self.tag + 1
        return True

    def pop(self):  # a whole pop, run without interruption
        while True:
            seen = self.read()
            if self.cas(seen, self.next[seen[0]]):
                return seen[0]

    def push(self, n):
        while True:
            seen = self.read()
            self.next[n] = seen[0]
            if self.cas(seen, n):
                return

    def contents(self, limit=6):
        out, n = [], self.head
        while n is not None and len(out) < limit:
            out.append(n)
            n = self.next[n]
        return " -> ".join(out) + (" -> ..." if n is not None else "")


if __name__ == "__main__":
    for tagged in (False, True):
        s = Stack(["A", "B", "C"], tagged)
        print("tagged head" if tagged else "bare head", "| start:", s.contents())
        seen = s.read()  # thread 1 begins a pop: it reads the head A ...
        second = s.next[seen[0]]  # ... and A's successor B; then it is preempted
        a, b = s.pop(), s.pop()  # thread 2 pops A and B ...
        s.push(a)  # ... and pushes A back
        print(f"  thread 2 popped {a}, {b}, pushed {a} back:", s.contents())
        ok = s.cas(seen, second)  # thread 1 resumes: is the head still what it read?
        verdict = "succeeds" if ok else "fails"
        print(f"  thread 1's compare-and-swap {verdict}:", s.contents())
        if ok:
            print(f"  thread 1 returns {seen[0]}, and {second} is on the stack"
                  " while thread 2 still holds it")
        else:
            print(f"  thread 1 retries and pops {s.pop()}:", s.contents())
