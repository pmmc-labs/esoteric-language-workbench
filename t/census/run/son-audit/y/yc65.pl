use v5.42;
my $x=1; my %h = (a => $x, b => $x++); print "$h{a}$h{b}\n";
