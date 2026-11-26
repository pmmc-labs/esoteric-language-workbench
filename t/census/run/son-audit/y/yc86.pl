use v5.42;
my $x=1; my %h; $h{$x} = $x++; print join(",", %h), "\n";
