use v5.42;
my $h = {}; my $ok = ($h->{a} = 1) && $h->{a} + ($h->{a} = 5); print "$ok\n";
