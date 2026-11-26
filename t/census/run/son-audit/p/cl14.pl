use v5.42;
my $x = "a\n"; my $g = sub { $x }; chomp $x; print "[", $g->(), "]\n";
