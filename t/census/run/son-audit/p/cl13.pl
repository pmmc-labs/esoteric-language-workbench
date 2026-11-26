use v5.42;
my $x = "a"; my $g = sub { $x }; $x =~ s/a/b/; print $g->(), "\n";
