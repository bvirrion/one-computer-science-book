"""Exercises of the chapter on the halting problem."""
import ast
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from repeat_detector import state  # noqa: E402
from toymachine import Machine, assemble  # noqa: E402


def count_functions(path):                                   # exercise 5
    tree = ast.parse(Path(path).read_text())
    return sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               for n in ast.walk(tree))


def first_repeat(text):                                      # exercise 8
    """Step at which a state is met again, and the length of the cycle; or None."""
    m, seen = Machine(assemble(text)), {}
    while not m.halted:
        s = state(m)
        if s in seen:
            return m.steps, m.steps - seen[s]
        seen[s] = m.steps
        m.step()
    return None


def short_is_stopping(program, data):                        # exercise 10
    return len(inspect.getsource(program)) < 200


MULTIPLY = """
        IN    R0          ; a
        IN    R1          ; b
        LOADI R2, 0       ; the product
        LOADI R3, 1
        CMP   R1, R2      ; b = 0? (R2 is 0 here)
        JZ    done
loop:   ADD   R2, R0      ; product = product + a
        SUB   R1, R3      ; b = b - 1
        JNZ   loop
done:   OUT   R2
        HALT
"""


def multiply(a, b):                                          # exercise 14
    m = Machine(assemble(MULTIPLY), inputs=[a, b])
    m.run()
    return m.outputs[0]


def diagonal_flip(table):                                    # exercise 4
    """table[i][j]: does program i stop on input j? A row unlike every row."""
    return [not table[i][i] for i in range(len(table))]
