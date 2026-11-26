use v5.42;
my $x=1; sub f { my ($p)=@_; sub { $p } } my $c=f($x); $x=9; print $c->(), "\n";
