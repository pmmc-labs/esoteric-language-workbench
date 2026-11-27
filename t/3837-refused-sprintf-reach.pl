# kind: refused
# perl prints 9-0: sprintf's list for D109, through a sub.
use v5.42;
my $r = [1];
sub bump($t) { $t->[0] = 9; return 0; }
say sprintf("%s-%s", $r->[0], bump($r));
