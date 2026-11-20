# capture: session copy=vec.h,vec.c,fixed.c,vec_demo.c
gcc -std=c17 -O2 -Wall -Wextra vec_demo.c vec.c -o demo_vec
gcc -std=c17 -O2 -Wall -Wextra vec_demo.c fixed.c -o demo_fixed
./demo_vec | sed -n '15,18p'
./demo_fixed 2>&1 | sed -n '15,18p'
