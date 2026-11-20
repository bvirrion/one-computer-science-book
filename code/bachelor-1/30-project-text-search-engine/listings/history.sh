# capture: session copy=Makefile,make_corpus.py,tokenize.h,tokenize.c,folder.h,folder.c,index.h,index.c,query.h,query.c,topk.h,topk.c,scan.h,scan.c,main.c,naive.c,measure.c,units_test.c
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_AUTHOR_NAME="Ada Lovelace" GIT_AUTHOR_EMAIL=ada@example.org GIT_COMMITTER_NAME="Ada Lovelace" GIT_COMMITTER_EMAIL=ada@example.org GIT_AUTHOR_DATE="2026-03-02T09:00:00+0000" GIT_COMMITTER_DATE="2026-03-02T09:00:00+0000" # hidden
mkdir search && cd search && git init -q -b main # hidden
printf 'search\nnaive\nmeasure\nunits_test\n*.o\ncorpus/\nqueries.txt\n' > .gitignore # hidden
cp ../make_corpus.py ../folder.[ch] ../tokenize.[ch] ../topk.[ch] ../scan.[ch] ../query.[ch] ../naive.c . # hidden
git add . && git commit -q -m "Specify search; generate the corpus; the naive scan" # hidden
cp ../index.[ch] . && git add . && git commit -q -m "Build the inverted index" # hidden
cp ../main.c . && git add . && git commit -q -m "Answer AND queries from the index, the best ten" # hidden
cp ../Makefile ../units_test.c ../measure.c . && git add . && git commit -q -m "Makefile, unit tests, measurement" # hidden
git log --oneline
git show --stat --format='%s' HEAD~2 | head -5
make -s && ./units_test
git status --short | wc -l
