use v5.42;
my $o={l=>[1,2]}; my @b=(@{$o->{l}}, $o->{l}[0]=9); print "@b\n";
