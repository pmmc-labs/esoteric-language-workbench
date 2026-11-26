# kind: refused
# perl: a syntax error (T192).
use v5.42;
my $n = 0;
$n += $_ for 1 .. 3 if 1;
