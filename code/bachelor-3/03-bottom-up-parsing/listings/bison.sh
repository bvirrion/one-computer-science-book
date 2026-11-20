# capture: session copy=ifelse.y,lr.y
bison --version | head -n 1
bison -o ifelse.c ifelse.y
wc -l ifelse.c
bison --report=state -o lr.c lr.y
grep -c '^State' lr.output
bison -D lr.type=canonical-lr --report=state -o lr.c lr.y
grep -c '^State' lr.output
