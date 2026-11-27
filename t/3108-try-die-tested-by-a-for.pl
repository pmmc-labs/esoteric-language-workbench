# kind: refused
# perl warns of a precedence problem.
use v5.42;
for (my $i = 0; die "f\n"; $i++) { say $i; }
