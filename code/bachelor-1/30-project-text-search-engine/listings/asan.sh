# capture: session copy=Makefile,make_corpus.py,tokenize.h,tokenize.c,folder.h,folder.c,index.h,index.c,query.h,query.c,topk.h,topk.c,scan.h,scan.c,main.c,naive.c,measure.c,units_test.c
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 # hidden
python3 make_corpus.py corpus > /dev/null # hidden
S=-fsanitize=address,undefined
make -s search CFLAGS="-std=c17 -O1 -g $S" LDLIBS="-lm $S"
./search corpus nodo beli | head -3
./search corpus; echo "exit status $?"
