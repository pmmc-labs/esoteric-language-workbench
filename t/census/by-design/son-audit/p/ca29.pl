use v5.42;
my @o; sub DESTROY { push @o, "d" } { my $x = bless [], "main"; } print "@o\n";
