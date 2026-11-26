use v5.42;
my $n=0; my $r; $r=sub { $n++; $r->() if $n<4; $n }; print $r->(),"\n";
