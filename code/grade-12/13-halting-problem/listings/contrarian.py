"""The program of the proof. Given any function that claims to decide halting,
it builds a program on which that function is wrong."""


def make_contrarian(halts):
    """halts(program, data) claims to say whether program(data) ever stops."""

    def contrarian(program):
        if halts(program, program):              # "program stops on itself"
            while True:                          # then run for ever
                pass
        return "stopped"                         # else stop at once

    return contrarian
