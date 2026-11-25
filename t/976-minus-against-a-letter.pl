# kind: refused
# perl prints u: -e is the file test, of a file called 2 (T135).
use v5.42;
sub e($p) { return $p + 10; }
my $n = -e(2);
say defined($n) ? "d" : "u";
