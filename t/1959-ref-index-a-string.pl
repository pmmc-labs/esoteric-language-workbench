# kind: refused
# perl runs it ('1\n') and warns: Argument 'x' isn't numeric in array element.
use v5.42;
my $r = [1, 2];
say $r->["x"];
