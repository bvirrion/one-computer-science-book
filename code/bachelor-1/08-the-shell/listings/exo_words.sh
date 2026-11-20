# capture: session
export LC_ALL=C # hidden
f="a b"; g='*'; touch x.txt
printf '[%s]' $f "$f" '$f'; echo
printf '[%s]' $g "$g"; echo
printf '[%s]' "$f"$f "" $empty; echo
printf '[%s]' a\ b "c d"e'f g'; echo
