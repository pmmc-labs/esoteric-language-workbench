# kind: refused
# perl: Global symbol "$x" requires explicit package name (T134).
use v5.42;
sub bump() { $x++; }
my $x;
bump();
