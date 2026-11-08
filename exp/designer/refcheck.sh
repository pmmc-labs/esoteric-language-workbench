#!/usr/bin/env bash
# Run the referee over a Ditto checkout's golden tests; print disagreements.
root=$1 ref=$2; cd "$root"
one() {
  t=$1 b=${t%.ditto}; in=/dev/null; [[ -f $b.stdin ]] && in=$b.stdin
  got=$( { timeout 60 python3 -I "$ref" "$t" <"$in" 2>&1; s=$?; (( s )) && echo "exit: $s"; } )
  [[ "$got" == "$(cat $b.expected)" ]] || echo "DIFF $t"
}
export -f one; export ref
ls t/*.ditto examples/*.ditto 2>/dev/null | xargs -P8 -I{} bash -c 'one {}' | sort
echo "total $(ls t/*.ditto examples/*.ditto 2>/dev/null | wc -l)"
