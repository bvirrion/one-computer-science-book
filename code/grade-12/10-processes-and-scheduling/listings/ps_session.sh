# capture: session
sleep 30 &
sleep 1
ps -o state=,comm= -p $!
ps -o state=,comm= -p $$
