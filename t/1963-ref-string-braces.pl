# kind: refused
# perl runs it: '1 2\n'.
use v5.42;
my $r = [1, 2];
say "@{$r}";
