# kind: refused
# perl dies: not a HASH reference (T203).
use v5.42;
my $x = 3;
say "$x->{a}";
