use v5.42;
my $r=eval { eval { die "a\n" }; "v:$@" }; print $r;
