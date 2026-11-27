# kind: refused
# perl runs it, and says nothing.
use v5.42;
my %h = (a => 1);
my $r = \%h;
my @l = ($r->{a}, delete $h{a});
