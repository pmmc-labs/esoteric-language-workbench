use v5.42;
my $o={l=>[1,2]}; sub z { $o->{l}[1]=7 } for my $x (@{$o->{l}}) { z(); print $x } print "\n";
