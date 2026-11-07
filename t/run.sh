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

# Paths given on the command line are relative to where the caller stands.
args=()
for p in "$@"; do
  [[ $p == --one ]] || p=$(realpath --relative-to="$root" "$p")
  args+=("$p")
done
cd "$root" || exit 2
mkdir -p "$outdir"

if [[ ${args[0]:-} == --one ]]; then
  run_one "${args[1]}"
  exit
fi

tests=()
if (( ${#args[@]} > 0 )); then
  tests=("${args[@]}")
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
fails=$(printf '%s\0' "${tests[@]}" | xargs -0 -n1 -P "$jobs" "$root/t/run.sh" --one)
status=$?
# xargs exits 123 when a run exited 1 (a failed test); anything else is a
# problem with the runner itself, and must not read as a pass.
if (( status != 0 && status != 123 )) || { (( status == 123 )) && [[ -z $fails ]]; }; then
  echo "$tag: the runner failed (xargs status $status)"
  exit 2
fi
if [[ -n $fails ]]; then
  if [[ -n ${DITTO_DIFF:-} ]]; then echo "$fails"; else echo "$fails" | sort; fi
  nfail=$(echo "$fails" | grep -c '^FAIL ')
  echo "$tag: $nfail of ${#tests[@]} failed"
  exit 1
fi
echo "$tag: ${#tests[@]} passed"
