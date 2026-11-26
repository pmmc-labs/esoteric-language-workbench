#!/bin/sh
# Reruns every .pl here under perl 5.42 and writes outputs.txt.
#     sh run-all.sh
cd "$(dirname "$0")"
PERL=${CURLY_PERL:-/opt/perl-5.42/bin/perl}
: > outputs.txt
for f in w1.pl w1b.pl g1.pl g1b.pl n1-*.pl n2.pl n2b.pl s-*.pl same-as-dot.pl; do
    echo "=== $f" >> outputs.txt
    timeout 20 "$PERL" "$f" > .out 2> .err; code=$?
    sed 's/^/out: /' .out >> outputs.txt
    sed 's/^/err: /' .err >> outputs.txt
    echo "exit: $code" >> outputs.txt
done
rm -f .out .err
