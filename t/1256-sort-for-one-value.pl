# kind: refused
# perl: undef, and a warning (T178, D84).
use v5.42;
my @a = (3, 1, 2);
my $s = sort { $a <=> $b } @a;
