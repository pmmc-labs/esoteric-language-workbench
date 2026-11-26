use v5.42;
eval { die "a\n" }; my $e1 = $@; eval { 1 }; print "[$e1][$@]", "\n";
