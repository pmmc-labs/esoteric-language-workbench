use v5.42;
my $x=1; sub f { my @c=@_; return \@c } my $r=f($x); $r->[0]=9; print "$x\n";
