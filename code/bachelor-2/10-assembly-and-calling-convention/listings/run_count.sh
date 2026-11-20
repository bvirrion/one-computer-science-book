# capture: session copy=count.S
for c in 7 4006 978030640; do echo $c | python -m rv run count.S --stats | sed -n 2,4p; done
