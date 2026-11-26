use v5.42;
my $r = eval { eval { die "in\n" }; "v:$@" }; print $r;
