# kind: refused
# perl runs it: '2\n'.
use v5.42;
my $r = {a => 1};
my @l = ($r->{a}, delete $r->{a});
say scalar(@l);
