use v5.42;
my $x = 1; { my $x = $x + 1; { my $x = $x * 10; print $x } print $x } print "$x\n";
