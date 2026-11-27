# kind: refused
# perl runs it ('7\n') and warns: Use of uninitialized value in say.
use v5.42;
my $r = [1, 2];
say $r->[0], ($r = [7, 8, 9])->[0];
