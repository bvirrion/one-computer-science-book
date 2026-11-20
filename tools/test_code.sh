#!/usr/bin/env bash
# Run every code test of the series, of one year, or of one chapter:
#   tools/test_code.sh                          everything (main session only, after the books land)
#   tools/test_code.sh grade-8                  one year
#   tools/test_code.sh grade-8/04-searching-and-sorting   one chapter
#   python : ruff + pytest, one process per tests/ directory
#   C      : every *_test.c built with gcc -std=c17 -O2 -Wall -Wextra -Werror (plus the chapter's .c files
#            named in its first-line `// test-with: a.c b.c`) and run
#   C++    : every *_test.cpp (plus the files named in its first-line `// test-with: a.cpp`) built with
#            g++ -std=c++20 -O2 -Wall -Wextra -Werror and run
#   Rust   : every *_test.rs outside a Cargo crate built with rustc --edition 2021 --test and run
#            (it reaches a listing with #[path = "../listings/x.rs"] mod x;)
#   Rust   : cargo clippy -D warnings + cargo test --offline in every dir holding a Cargo.toml
#   LaTeX  : every \omcode{path}{a}{b} points at an existing file and a..b is inside it, at most 40 lines
#   outputs: every \omoutput file reruns byte for byte (OCS_TESTS=fast: existence only)
set -uo pipefail
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONHASHSEED=0 TZ=UTC
PY=.venv/bin/python
sel="${1:-}"
roots=()
# a whole year or chapter directory is taken exactly (grade-1 must not also match grade-10..12);
# otherwise the selection is a prefix (grade-8/03 matches grade-8/03-<slug>)
if [ -n "$sel" ]; then
  sel=${sel%/}
  if [ -d "code/$sel" ]; then roots=("code/$sel"); sel="$sel/"
  elif [[ "$sel" != */* ]]; then echo "no code for $sel"; echo "TEST-CODE: GREEN"; exit 0
  else roots=(code/$sel*); fi
else roots=(code); fi
[ -e "${roots[0]}" ] || { echo "nothing under code/$sel"; exit 2; }
CAP=(); command -v systemd-run >/dev/null && [ -n "${XDG_RUNTIME_DIR:-}" ] && CAP=(systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0)
fail=0
say(){ printf '\n== %s\n' "$*"; }

say "ruff"
$PY -m ruff check -q "${roots[@]}" || fail=1

say "pytest"
npy=$(find "${roots[@]}" -name 'test_*.py' | wc -l)
if [ "$npy" -gt 0 ]; then
  echo "$npy test files"
  npass=0; nbad=0
  while IFS= read -r d; do
    yr=${d#code/}; yr=${yr%%/*}
    out=$(PYTHONPATH="code/shared/toymachine:code/shared/rv:code/shared/sqlrun:code/shared/town:code/shared/turtlerec:code/$yr/lib" \
          "${CAP[@]}" $PY -m pytest -q -p no:cacheprovider "$d" 2>&1); rc=$?
    if [ $rc -eq 0 ] || [ $rc -eq 5 ]; then
      npass=$((npass+1)); echo "ok   $d: $(tail -n 1 <<<"$out")"
    else
      nbad=$((nbad+1)); fail=1; echo "FAIL $d"; echo "$out"
    fi
  done < <(find "${roots[@]}" -type d -name tests -printf '%h\n' | sort -u)
  echo "pytest: $npass directories green, $nbad failing"
else echo "(no python tests)"; fi

tmp=$(mktemp -d)
trap 'rm -r -- "$tmp"' EXIT
say "C"
n=0
while IFS= read -r t; do
  n=$((n+1)); d=$(dirname "$t"); exe="$tmp/$(basename "${t%.c}")_$n"
  extra=$(head -1 "$t" | sed -n 's|^// test-with: *||p')
  srcs=("$t"); for e in $extra; do srcs+=("$d/$e"); done
  if gcc -std=c17 -O2 -Wall -Wextra -Werror -I"$d" -I"$d/../listings" "${srcs[@]}" -o "$exe" -lm \
     && (cd "$d" && timeout 300 "${CAP[@]}" "$exe"); then
    echo "ok   $t"; else echo "FAIL $t"; fail=1; fi
done < <(find "${roots[@]}" -name '*_test.c' | sort)
[ $n -eq 0 ] && echo "(no C tests)"

say "C++"
n=0
while IFS= read -r t; do
  n=$((n+1)); d=$(dirname "$t"); exe="$tmp/$(basename "${t%.cpp}")_$n"
  extra=$(head -1 "$t" | sed -n 's|^// test-with: *||p')
  srcs=("$t"); for e in $extra; do srcs+=("$d/$e"); done
  if g++ -std=c++20 -O2 -Wall -Wextra -Werror -I"$d" -I"$d/../listings" "${srcs[@]}" -o "$exe" -pthread \
     && (cd "$d" && timeout 300 "${CAP[@]}" "$exe"); then
    echo "ok   $t"; else echo "FAIL $t"; fail=1; fi
done < <(find "${roots[@]}" -name '*_test.cpp' | sort)
[ $n -eq 0 ] && echo "(no C++ tests)"

say "Rust"
n=0
while IFS= read -r c; do
  n=$((n+1)); d=$(dirname "$c")
  if (cd "$d" && CARGO_TARGET_DIR="$tmp/target_$n" cargo clippy -q --offline --all-targets -- -D warnings \
      && CARGO_TARGET_DIR="$tmp/target_$n" timeout 600 cargo test -q --offline >"$tmp/cargo_$n.log" 2>&1); then
    echo "ok   $d"; else grep -E "^test result|FAILED|panicked|^error" "$tmp/cargo_$n.log" | head -20; echo "FAIL $d"; fail=1; fi
done < <(find "${roots[@]}" -name Cargo.toml -not -path '*/target/*' | sort)
while IFS= read -r t; do
  n=$((n+1)); d=$(dirname "$t"); exe="$tmp/$(basename "${t%.rs}")_$n"
  if [ -n "$(find "$d" -maxdepth 2 -name Cargo.toml | head -1)" ]; then continue; fi
  if rustc --edition 2021 -O --test -D warnings "$t" -o "$exe" \
     && (cd "$d" && timeout 300 "${CAP[@]}" "$exe" -q --test-threads=1); then
    echo "ok   $t"; else echo "FAIL $t"; fail=1; fi
done < <(find "${roots[@]}" -name '*_test.rs' -not -path '*/target/*' | sort)
[ $n -eq 0 ] && echo "(no Rust tests)"

say "\\omcode ranges"
python3 tools/check_omcode.py "$sel" || fail=1

say "outputs"
if [ "${OCS_TESTS:-all}" = fast ]; then python3 tools/check_outputs.py --no-run "$sel" || fail=1
else python3 tools/check_outputs.py "$sel" || fail=1; fi

[ $fail -eq 0 ] && echo && echo "TEST-CODE: GREEN" || { echo; echo "TEST-CODE: RED"; exit 1; }
