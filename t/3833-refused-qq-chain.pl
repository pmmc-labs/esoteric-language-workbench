# kind: refused
# perl prints 1: a dereference in qq waits for step 13d, as in double quotes.
use v5.42;
my $r = [1];
say qq{$r->[0]};
