# capture: session copy=saxpy.c
gcc -O3 -fopt-info-vec-optimized -c saxpy.c
gcc -O3 -fopt-info-vec-missed -c saxpy.c 2>&1 | grep -E '^saxpy.c:1[01]'
gcc -O3 -S -o - saxpy.c | grep -E 'mulps|addps|mulss|addss'
