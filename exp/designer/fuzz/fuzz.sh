#!/usr/bin/env bash
# DITTO_ROOT=CHECKOUT fuzz.sh N START   (GEN_ARGS="--else" to include the else operator;
# REFEREE overrides ../referee/referee.py)
N=${1:?N}; START=${2:-1}
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$HERE/work" "$HERE/diffs"; mkdir -p "$HERE/work" "$HERE/diffs"
seq "$START" $((START + N - 1)) | xargs -P 8 -n1 "$HERE/one.sh"
cat "$HERE"/work/*.res > "$HERE/results.txt"
echo "total: $(wc -l < "$HERE/results.txt")"
echo "agreed: $(grep -c ' agree ' "$HERE/results.txt")  disagreed: $(grep -c ' DIFF ' "$HERE/results.txt")"
# outcome by referee's exit status; ok = no exit line
for c in ok fault compile timeout other; do echo "$c: $(grep -c " $c\$" "$HERE/results.txt")"; done
echo "genfail: $(grep -c GENFAIL "$HERE/results.txt")"
