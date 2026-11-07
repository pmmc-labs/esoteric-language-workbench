#!/usr/bin/env bash
# Golden test runner. Usage: t/run.sh [test.ditto ...]
# With no arguments, runs every t/*.ditto and examples/*.ditto in parallel.
# Environment: T_TAG names the build directory (build/golden-$T_TAG),
# LANG_CC and LANG_CFLAGS are passed through to bin/ditto.
# The expected file is stdout and stderr together, plus "exit: N" when N != 0.
set -u
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
tag=${T_TAG:-cc}
outdir=$root/build/golden-$tag

run_one() {
  local test=$1 base name exe got status stdin
  base=${test%.ditto}
  name=$(basename "$base")
  exe=$outdir/$name
  got=$outdir/$name.out
  {
    "$root/bin/ditto" build "$test" -o "$exe" 2>&1
    status=$?
    if (( status == 0 )); then
      stdin=/dev/null
      [[ -f $base.stdin ]] && stdin=$base.stdin
      "$exe" <"$stdin" 2>&1
      status=$?
    fi
    if (( status != 0 )); then echo "exit: $status"; fi
  } >"$got"
  if [[ ! -f $base.expected ]] || ! cmp -s "$got" "$base.expected"; then
    echo "FAIL $test"
    if [[ -n ${DITTO_DIFF:-} ]]; then
      diff <(cat "$base.expected" 2>/dev/null) "$got" | head -20 | sed 's/^/    /'
    fi
    return 1
  fi
}

cd "$root" || exit 2
mkdir -p "$outdir"

if [[ ${1:-} == --one ]]; then
  run_one "$2"
  exit
fi

tests=()
if (( $# > 0 )); then
  for p in "$@"; do
    tests+=("$(realpath --relative-to="$root" "$(cd "$OLDPWD" && realpath "$p")")")
  done
  export DITTO_DIFF=1
else
  shopt -s nullglob
  tests=(t/*.ditto examples/*.ditto)
fi

if (( ${#tests[@]} == 0 )); then
  echo "$tag: no tests"
  exit 0
fi

jobs=$(nproc 2>/dev/null || echo 4)
fails=$(printf '%s\0' "${tests[@]}" | xargs -0 -n1 -P "$jobs" "$0" --one)
if [[ -n $fails ]]; then
  echo "$fails" | sort
  nfail=$(echo "$fails" | grep -c '^FAIL ')
  echo "$tag: $nfail of ${#tests[@]} failed"
  exit 1
fi
echo "$tag: ${#tests[@]} passed"
