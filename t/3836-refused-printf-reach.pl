# kind: refused
# perl prints 55: printf's list for D109.
use v5.42;
my $r = [1];
printf("%s%s\n", $r->[0], ($r->[0] = 5));
