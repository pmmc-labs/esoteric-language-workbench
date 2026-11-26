use v5.42;
my @r; for my $x (1..2) { for (qw(a b)) { push @r,"$x$_" } } print "@r\n";
