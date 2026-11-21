"""Tests of our assembler and simulator, against the shared package."""
import sys
import unittest
from pathlib import Path

from assembler_m2 import assemble
from simulator_m4 import new_machine, run

CODE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CODE / "shared" / "toymachine"))
import toymachine

FOLDER = CODE / "grade-11" / "02-von-neumann-machine" / "listings"
PROGRAMS = sorted(FOLDER.glob("*.toy"))
BAD = {"unknown instruction": "LOADX R0, 1", "undefined label": "JMP nowhere",
       "too large": "LOADI R0, 300", "bad register": "ADD R0, R7",
       "twice": "a: NOP\na: NOP", "operands": "ADD R0"}


class OursTests(unittest.TestCase):
    def test_same_bytes(self):
        for path in PROGRAMS:
            with self.subTest(path.name):
                text = path.read_text()
                self.assertEqual(assemble(text), toymachine.assemble(text))

    def test_errors_where_shared_errs(self):
        for name, text in BAD.items():
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    assemble(text)
                with self.assertRaises(toymachine.ToyError):
                    toymachine.assemble(text)

    def test_flags_of_every_addition(self):
        for a in range(0, 256, 5):
            for b in range(0, 256, 7):
                text = f"LOADI R0, {a}\nLOADI R1, {b}\nADD R0, R1\nHALT"
                m = new_machine(assemble(text))
                run(m)
                shared = toymachine.Machine(toymachine.assemble(text))
                shared.run()
                self.assertEqual((m["reg"], m["flags"]), (shared.reg, shared.flags))

    def test_step_limit(self):
        with self.assertRaises(RuntimeError):
            run(new_machine(assemble("again: JMP again")), max_steps=100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
