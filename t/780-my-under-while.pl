# kind: refused
# perl makes the variable undef again each time round, and it is undef
# after the loop (T119).
use v5.42;
my $i = 0;
my $x = 5 while $i++ < 3;
