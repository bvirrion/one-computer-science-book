from tokens import parse_number, read_program

SOURCE = """\
; a comment line
start:  LOADI R0, 0x2A    ; 42
        LOADI R1, ';'     ; a quoted ; is a character
        ADDI  R0, -3
end:    HALT
table:  DATA 0b101, 'A', 7
"""
for row in read_program(SOURCE):
    print(row)
for tok in ["42", "0x2A", "0b101010", "'*'", "-3", "300", "4x"]:
    try:
        print(f"{tok:>9} -> {parse_number(tok, 1)}")
    except ValueError as error:
        print(f"{tok:>9} -> ValueError: {error}")
